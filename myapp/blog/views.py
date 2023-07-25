from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q
from django.core.files.storage import default_storage
from django.http import JsonResponse
from .models import Post, Review, Tag
from user.models import Profile
# from user.models import BusinessUser
from .forms import PostForm, ReviewForm, TagForm, SearchForm
# Create your views here.


### Post
class Index(View):
    def get(self, request):
        # print(request.user.username)
        post_objs = Post.objects.all().order_by('-created_at')
        profile = Profile.objects.filter(user__in=[post.writer for post in post_objs])
        # print(profile[0].image.url)
        # print(post_objs.qeury)
        context = {
            'posts':post_objs,
            'profile': profile,
            'title':'Blog'
        }
        
        return render(request, 'blog/post_list.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = Post.objects.prefetch_related('review_set').get(pk=pk)
        profile = Profile.objects.get(user=post.writer)
        reviews = post.review_set.all()
        review_form = ReviewForm()
        tags = post.tags.all()
        tag_form = TagForm()
        post.count += 1
        post.save()
        like_count = post.like_users.count()
        # print(post.like_users.all())
        like_exist = post.like_users.all()
        #     # print(request.user in post.like_users.all())
        #     like_exist = True
        context = {
            'title' : 'Blog',
            'post_id' : pk,
            'post_title' : post.title,
            'post_content' : post.content,
            'post_writer' : post.writer,
            'post_created_at' : post.created_at,
            'post_name': post.name,
            'post_count':post.count,
            'like_count':like_count,
            'like_exist':like_exist,
            # 'post_img':post.image.url,
            'reviews' : reviews,
            'review_form' : review_form,
            'tags' : tags,
            'tag_form':tag_form,
            'profile':profile
        }
        if post.image:  # 이미지가 있는 경우에만 context에 추가합니다.
            context['post_img'] = post.image.url
        return render(request, 'blog/post_detail.html', context)


class Write(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_form.html', context)
        # else:
        #     return redirect('blog:list')
            
    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.name = request.user.name
            post.address = request.user.fulladdress
            # if 'image' in request.FILES:
            # post.content = request.POST.get('content', '')  
            post.save()
            return redirect('blog:list')
        
        context = {
            'form':form
        }
        return render(request, 'blog/post_form.html', context)


class Update(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        
        form = PostForm(initial={'title':post.title, 'content':post.content, 'image':post.image})
        context = {
            'title':'Blog',
            'form':form,
            'post':post
        }
        return render(request, 'blog/post_edit.html', context)
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, request.FILES)
        # if post.image and 'image' in request.FILES:
        #     default_storage.delete(post.image.path)
        # content_data = request.POST.get('content', '')
        # post.content = content_data
        if form.is_valid():
            # post.title = form.cleaned_data['title']
            # post.content = form.cleaned_data['content']
            # image_file = request.FILES.get('image')
            post.title = request.POST['title']
            post.content = request.POST['content']
            print(post.content)
            print("Form data before save:", form.cleaned_data)

            post.save()
            
            print("Form data after save:", form.cleaned_data)
            return redirect('blog:detail', pk=pk)
        
        context = {
            'form': form,
            'post': post
        }
        return render(request, 'blog/post_detail.html', context)


class Delete(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('blog:list')


### Review
class ReviewWrite(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Post does not exist.', str(e))
        
        reviews = Review.objects.select_related('post')
        if form.is_valid():
            content = form.cleaned_data['content']
            writer = request.user
            try:
                review = Review.objects.create(post=post, content=content, writer=writer)
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
            except ValidationError as e:
                print('Validation error occurred', str(e))                
            return redirect('blog:detail', pk=pk)
        tag_form = TagForm()
        context = {
            'title': 'Blog',
            'post_id': pk,
            'post_title': post.title,
            'post_content' : post.content,
            'post_name' : post.name,
            'post_created_at' : post.created_at,
            'reviews' : post.review_set.all(),
            'review_form' : form,
            'tags': post.tag_set.all(),
            'tag_form': tag_form
        }
        return render(request, 'blog/post_detail.html', context)


class ReviewDelete(View):
    def post(self, request, pk):
        try:
            review = Review.objects.get(pk = pk)
        except ObjectDoesNotExist as e:
            print('Comment does not exist', str(e))
        post_id = review.post.id
        review.delete()
        
        return redirect('blog:detail', pk = post_id)


### Tag

class TagWrite(View):
    def post(self, request, pk):
        form = TagForm(request.POST)
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            print('Tag Does not exist', str(e))
        reviews = Review.objects.select_related('post')
        tags = Tag.objects.select_related('post')
        
        if form.is_valid():
            name = form.cleaned_data['name']
            writer = request.user
            try:
                tag = Tag.objects.create(post = post, name=name, writer = writer)
            except ObjectDoesNotExist as e:
                print('Post does not exist.', str(e))
            
            except ValidationError as e:
                print('Valdation error occurred', str(e))
            # FK로 연결된 애들은 객체상태로 넘겨줘야 됩니다. 
            # comment = Comment(post = post) => comment.save()
            return redirect('blog:detail', pk=pk)
        # form.add_error(None, '폼이 유효하지 않습니다.')
        review_form = ReviewForm()
        context = {
            'title': 'Blog',
            'post_id': pk,
            'post_title': post.title,
            'post_content' : post.content,
            'post_name' : post.name,
            'post_created_at' : post.created_at,
            'reviews' : post.review_set.all(),
            'hashtags' : post.tag_set.all(),
            'review_form' : review_form,
            'tag_form' : form
            
        }
        return render(request, 'blog/post_detail.html', context)


class TagDelete(View):
    def post(self, request, pk):
        # pk는 hashtag의 pk (hashtag_id)
        # 해시태그 불러오기
        try:
            tag = Tag.objects.get(pk = pk)
            
        except ObjectDoesNotExist as e:
            print('HashTag does not exist.', str(e))
        # 해쉬태그에 담겨 있는 FK의 포스트 pk 값 가져오기
        post_id = tag.post.id
        
        # 해시태그 삭제 하기전에 값을 가져와야됩니다.
        tag.delete()
        
        return redirect('blog:detail', pk = post_id)

class SearchTag(View):
    def get(self, request, tag):
        category = request.GET.get('category')
        q = request.GET.get('q')
        
        if not q:  # 검색어가 없는 경우
            queryset = Post.objects.all()  # 모든 게시물
        else:
            # 선택한 카테고리에 따라 필터링
            if category == 'address':
                queryset = Post.objects.filter(address__icontains=q)
            elif category == 'tag':
                queryset = Post.objects.filter(tags__name__icontains=q)
            elif category == 'content':
                queryset = Post.objects.filter(content__icontains=q)
            else:
                queryset = Post.objects.none()  # 선택하지 않은 경우 빈 쿼리셋 반환
        context = {
            'posts': queryset,
            'q': q,
            'title': 'Blog',
        }
        return render(request, 'blog/post_list.html', context)


class LikePost(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        post = get_object_or_404(Post, pk=post_id)

        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
            # liked = False  # 이 줄은 삭제합니다.
        else:
            post.like_users.add(request.user)
            # liked = True  # 이 줄은 삭제합니다.

        return redirect('blog:detail', pk=post_id)


# 비동기 통신 
# class LikePost(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         post_id = kwargs['pk']
#         post = get_object_or_404(Post, pk=post_id)

#         if request.user in post.like_users.all():
#             post.like_users.remove(request.user)
#             liked = False
#         else:
#             post.like_users.add(request.user)
#             liked = True

#         # 좋아요 상태와 좋아요 수를 JSON 형태로 반환합니다.
#         response_data = {
#             'liked': liked,
#             'like_count': post.like_users.count(),
#         }
#         print(post.like_users.count())
#         return JsonResponse(response_data)