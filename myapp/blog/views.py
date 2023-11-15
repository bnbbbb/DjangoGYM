from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from django.core.files.storage import default_storage
from .models import Post, Review, Tag
from .models import PostImage as Image
from user.models import Profile, User

from urllib.parse import urlparse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import PostSerializer, TagSerializer, PostImageSerializer
from user.serializers import UserSerializer, ProfileSerializer
from user.models import User, Profile
import markdown
from .upload import S3ImgUploader
from .imgconfirm import img_objects
from rest_framework.renderers import JSONRenderer
from bs4 import BeautifulSoup
from rest_framework.pagination import PageNumberPagination

# Create your views here.


### Post
class List(APIView):
    pagination_class = PageNumberPagination
    def get(self, request):
        posts = Post.objects.filter(is_active = True)
        paginated_queryset = self.pagination_class().paginate_queryset(posts, request, view=self)
        data = []
        post_images = [obj['Key'] for obj in img_objects.get('Contents', []) if obj['Key'].startswith('post/')]
        post_img = [image.image for image in Image.objects.all()]
        img_confirm = [image for image in post_images if image not in post_img]
        for del_img in img_confirm:
            delete_img = S3ImgUploader(del_img)
            delete_img.delete()
            img_confirm = []
            
        for post in paginated_queryset:
            profile = Profile.objects.get(user=post.writer)
            post_img = Image.objects.filter(post=post).first()
            if post_img:
                image_url = post_img.image
            else:
                image_url = None
            profileserializer = ProfileSerializer(profile).data
            serializer = PostSerializer(post).data
            tags = Tag.objects.filter(post=post.id).values()
            html_text = markdown.markdown(post.content)
            soup = BeautifulSoup(html_text, 'html.parser')
            plain_text = soup.get_text()
            
            post_info = {
                'id' : post.id,
                'content' : plain_text, 
                'title' : post.title,
                'name' : post.name,
                'writer': post.writer_id,
                "post" : serializer,
                'tags' : tags,
                'created_at': post.created_at, 
                'first_img' : image_url
            }
            add_post = {
                'post' : post_info,
                'writer': profileserializer,
            }
            data.append(add_post)
        data = {
            'posts' : data,
            'post_len' : len(posts)
        }
        return Response(data, status=status.HTTP_200_OK)


class SearchTag(APIView):
    pagination_class = PageNumberPagination
    
    def get(self, request, searchTerm):
        if not searchTerm:
            post_results = Post.objects.filter(is_active = True)
        else:
            writer_results = Profile.objects.filter(
                Q(address__contains = searchTerm)|
                Q(name__contains = searchTerm)
            )
            post_results = Post.objects.filter(
                Q(title__contains=searchTerm) | 
                Q(content__contains=searchTerm) |
                Q(writer__id__in = writer_results) 
            )
        data = []
        paginated_queryset = self.pagination_class().paginate_queryset(post_results, request, view=self)
        
        for post in paginated_queryset:
            if post.is_active == False:
                continue
            profile = Profile.objects.get(user=post.writer)
            profileserializer = ProfileSerializer(profile).data
            serializer = PostSerializer(post).data
            tags = Tag.objects.filter(post=post.id).values()
            html_text = markdown.markdown(post.content)
            soup = BeautifulSoup(html_text, 'html.parser')
            plain_text = soup.get_text()
            post_info = {
                'id' : post.id,
                'content' : plain_text, 
                'title' : post.title,
                'name' : post.name,
                'writer': post.writer_id,
                "post" : serializer,
                'tags' : tags,
                'created_at': post.created_at
            }
            add_post = {
                'post' : post_info,
                'writer': profileserializer,
            }
            data.append(add_post)
        data = {
            'posts' : data,
            'post_len' : len(post_results)
        }
        return Response(data, status=status.HTTP_200_OK, content_type="application/json")


class DetailView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        profile = Profile.objects.get(user=post.writer.id)
        writer_info = ProfileSerializer(profile).data
        # like = 
        tags = Tag.objects.filter(post=post.id).values()
        
        reviews_infos = []
        
        post_info = {
                'id' : post.id,
                'content' : post.content, 
                'title' : post.title,
                'created' : post.created_at,
            }
        post_data = PostSerializer(post).data
        data = {
            'post' : post_info,
            'writer' : writer_info,
            'tags' : tags
        }
        return Response(data, status = status.HTTP_200_OK)


class PostImage(APIView):
    def post(self, request):
        user = User.objects.get(username=request.user)
        post_imgs = []
        if request.FILES['image']:
            post_img = request.FILES['image']
            upload_lmg = S3ImgUploader(post_img)
            upload_url = upload_lmg.upload('post')
            post_imgs.append('https://myorgobucket.s3.ap-northeast-2.amazonaws.com/'+upload_url)
        return Response(post_imgs, status=status.HTTP_200_OK)


class Write(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user = User.objects.get(username=user)
        request_data = request.data.copy()
        request_data['writer'] = user.id
        serializer = PostSerializer(data=request_data)
        tags = request.data.get('tags').split('#')
        images = request.data.getlist('image')[0].split(',')
        if serializer.is_valid():
            post = serializer.save(is_active=True)
            if images != ['']:
                for image in images:
                    img_data = {
                        'post' : post.id,
                        'image' : image.split('.com/')[1]
                    }
                    img_serializer = PostImageSerializer(data=img_data)
                    if img_serializer.is_valid():
                        img_serializer.save()
                    
            for tag in tags:
                tag_data = {
                    'post' : post.id,
                    'name' : tag
                }
                tag_serializer = TagSerializer(data=tag_data)
                if tag_serializer.is_valid():
                    tag_serializer.save()
            data = {
                'message': '게시글 등록 완료',
            }
            return Response(data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Update(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        post_img = Image.objects.filter(post=pk)
        # toast_ui에 이미지가 지워지면 update할 때 postimg 모델에서 지움
        images_content = ''.join(request.data.get('content').split(','))
        for img in post_img:
            if str(img.image) not in images_content:
                img.delete()
        post.tags.all().delete()
        serializer = PostSerializer(post, data=request.data, partial=True)
        tags = request.data.get('tags').split(' ')
        images = request.data.getlist('image')[0].split(',')
        if serializer.is_valid():
            post = serializer.save()
            if images != ['']:
                for image in images:
                    img_data = {
                        'post' : post.id,
                        'image' : image.split('.com/')[1]
                    }
                    img_serializer = PostImageSerializer(data=img_data)
                    if img_serializer.is_valid():
                        img_serializer.save()
                    
            for tag in tags:
                tag_data = {
                    'post' : post.id,
                    'name' : tag
                }
                tag_serializer = TagSerializer(data=tag_data)
                if tag_serializer.is_valid():
                    tag_serializer.save()
            data = {
                'message' : '수정하였습니다.',
                'post' : serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        errors = serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class Delete(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = Post.objects.get(id = pk)
        # post.is_active = False
        # post.save()
        post.delete()
        data = {
            "message" : "글 삭제 완료",
            'post' : post.is_active
        }
        return Response(data, status=status.HTTP_200_OK)


### Review
# class ReviewWrite(View):
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
#         try:
#             post = Post.objects.get(pk=pk)
#         except ObjectDoesNotExist as e:
#             print('Post does not exist.', str(e))
        
#         reviews = Review.objects.select_related('post')
#         if form.is_valid():
#             content = form.cleaned_data['content']
#             writer = request.user
#             try:
#                 review = Review.objects.create(post=post, content=content, writer=writer)
#             except ObjectDoesNotExist as e:
#                 print('Post does not exist.', str(e))
#             except ValidationError as e:
#                 print('Validation error occurred', str(e))                
#             return redirect('blog:detail', pk=pk)
#         tag_form = TagForm()
#         context = {
#             'title': 'Blog',
#             'post_id': pk,
#             'post_title': post.title,
#             'post_content' : post.content,
#             'post_name' : post.name,
#             'post_created_at' : post.created_at,
#             'reviews' : post.review_set.all(),
#             'review_form' : form,
#             'tags': post.tag_set.all(),
#             'tag_form': tag_form
#         }
#         return render(request, 'blog/post_detail.html', context)


# class ReviewDelete(View):
#     def post(self, request, pk):
#         try:
#             review = Review.objects.get(pk = pk)
#         except ObjectDoesNotExist as e:
#             print('Comment does not exist', str(e))
#         post_id = review.post.id
#         review.delete()
        
#         return redirect('blog:detail', pk = post_id)

