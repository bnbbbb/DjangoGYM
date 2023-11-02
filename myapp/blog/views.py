from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from django.core.files.storage import default_storage
from .models import Post, Review, Tag
from user.models import Profile, User


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import PostSerializer, TagSerializer
from user.serializers import UserSerializer, ProfileSerializer
from user.models import User, Profile
import markdown
from rest_framework.renderers import JSONRenderer
from bs4 import BeautifulSoup


# from user.models import BusinessUser
# from .forms import PostForm, ReviewForm, TagForm, SearchForm
# Create your views here.


### Post
class List(APIView):
    def get(self, request):
        # user = Profile.objects.get(user = request.user)
        # print(request.user)
        posts = Post.objects.all()
        print(posts)
        data = []
        # print(post)
        for post in posts:
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
                # 'image' : post.image,
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
            'posts' : data
        }
        # print(data)
        return Response(data, status=status.HTTP_200_OK)


class SearchTag(APIView):
    def get(self, request, searchTerm):
        print(searchTerm)
        if not searchTerm:
            print(';12321')
            post_results = Post.objects.all()
        else:
            print('asdasdasd')
            writer_results = Profile.objects.filter(
                Q(address__contains = searchTerm)|
                Q(name__contains = searchTerm)
            )
            post_results = Post.objects.filter(
                Q(title__contains=searchTerm) | 
                Q(content__contains=searchTerm) |
                Q(writer__id__in = writer_results) 
            )
        print(post_results)
        data = []
        for post in post_results:
            # print(post.data)
            profile = Profile.objects.get(user=post.writer)
            profileserializer = ProfileSerializer(profile).data
            serializer = PostSerializer(post).data
            # print(serializer)
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
                # 'image' : post.image,
                "post" : serializer,
                'tags' : tags,
                'created_at': post.created_at
            }
            add_post = {
                'post' : post_info,
                'writer': profileserializer,
            }
            data.append(add_post)
            # print(data)
        data = {
            'posts' : data
        }
        # print(data)
        return Response(data, status=status.HTTP_200_OK, content_type="application/json")

#     def get(self, request, tag):
#         category = request.GET.get('category')
#         q = request.GET.get('q')
        
#         if not q:  # 검색어가 없는 경우
#             queryset = Post.objects.all()  # 모든 게시물
#         else:
#             # 선택한 카테고리에 따라 필터링
#             if category == 'address':
#                 queryset = Post.objects.filter(address__icontains=q)
#             elif category == 'tag':
#                 queryset = Post.objects.filter(tags__name__icontains=q)
#             elif category == 'content':
#                 queryset = Post.objects.filter(content__icontains=q)
#             else:
#                 queryset = Post.objects.none()  # 선택하지 않은 경우 빈 쿼리셋 반환
#         context = {
#             'posts': queryset,
#             'q': q,
#             'title': 'Blog',
#         }
#         return render(request, 'blog/post_list.html', context)


class DetailView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        profile = Profile.objects.get(user=post.writer.id)
        writer_info = ProfileSerializer(profile).data
        # like = 
        tags = Tag.objects.filter(post=post.id).values()
        
        reviews_infos = []
        
        # for review in reviews:
            # reviews_info = {}
        post_info = {
                'id' : post.id,
                'content' : post.content, 
                'title' : post.title,
                'created' : post.created_at,
            }
        post_data = PostSerializer(post).data
        data = {
            'post' : post_info,
            # 'review': reviews,
            'writer' : writer_info,
            'tags' : tags
        }
        return Response(data, status = status.HTTP_200_OK)


class Write(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user = User.objects.get(username=user)
        request_data = request.data.copy()
        request_data['writer'] = user.id
        serializer = PostSerializer(data=request_data)
        tags = request.data.get('tags').split('#')
        if serializer.is_valid():
            post = serializer.save(is_active=True)
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
        # post = Post.objects.get(id=request.data['post_id'])
        post.tags.all().delete()
        serializer = PostSerializer(post, data=request.data, partial=True)
        tags = request.data.get('tags').split(' ')
        print(tags)
        if serializer.is_valid():
            serializer.save()
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
    
    def post(self, request):
        post = Post.objects.get(id = request.data['post_id'])
        
        post.is_active = False
        post.save()
        print(post)
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


# ### Tag

# class TagWrite(View):
#     def post(self, request, pk):
#         form = TagForm(request.POST)
#         try:
#             post = Post.objects.get(pk=pk)
#         except ObjectDoesNotExist as e:
#             print('Tag Does not exist', str(e))
#         reviews = Review.objects.select_related('post')
#         tags = Tag.objects.select_related('post')
        
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             writer = request.user
#             try:
#                 tag = Tag.objects.create(post = post, name=name, writer = writer)
#             except ObjectDoesNotExist as e:
#                 print('Post does not exist.', str(e))
            
#             except ValidationError as e:
#                 print('Valdation error occurred', str(e))
#             # FK로 연결된 애들은 객체상태로 넘겨줘야 됩니다. 
#             # comment = Comment(post = post) => comment.save()
#             return redirect('blog:detail', pk=pk)
#         # form.add_error(None, '폼이 유효하지 않습니다.')
#         review_form = ReviewForm()
#         context = {
#             'title': 'Blog',
#             'post_id': pk,
#             'post_title': post.title,
#             'post_content' : post.content,
#             'post_name' : post.name,
#             'post_created_at' : post.created_at,
#             'reviews' : post.review_set.all(),
#             'hashtags' : post.tag_set.all(),
#             'review_form' : review_form,
#             'tag_form' : form
            
#         }
#         return render(request, 'blog/post_detail.html', context)


# class TagDelete(View):
#     def post(self, request, pk):
#         # pk는 hashtag의 pk (hashtag_id)
#         # 해시태그 불러오기
#         try:
#             tag = Tag.objects.get(pk = pk)
            
#         except ObjectDoesNotExist as e:
#             print('HashTag does not exist.', str(e))
#         # 해쉬태그에 담겨 있는 FK의 포스트 pk 값 가져오기
#         post_id = tag.post.id
        
#         # 해시태그 삭제 하기전에 값을 가져와야됩니다.
#         tag.delete()
        
#         return redirect('blog:detail', pk = post_id)

# class SearchTag(View):
#     def get(self, request, tag):
#         category = request.GET.get('category')
#         q = request.GET.get('q')
        
#         if not q:  # 검색어가 없는 경우
#             queryset = Post.objects.all()  # 모든 게시물
#         else:
#             # 선택한 카테고리에 따라 필터링
#             if category == 'address':
#                 queryset = Post.objects.filter(address__icontains=q)
#             elif category == 'tag':
#                 queryset = Post.objects.filter(tags__name__icontains=q)
#             elif category == 'content':
#                 queryset = Post.objects.filter(content__icontains=q)
#             else:
#                 queryset = Post.objects.none()  # 선택하지 않은 경우 빈 쿼리셋 반환
#         context = {
#             'posts': queryset,
#             'q': q,
#             'title': 'Blog',
#         }
#         return render(request, 'blog/post_list.html', context)