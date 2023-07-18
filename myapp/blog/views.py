from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Post, Review
# from user.models import BusinessUser
from .forms import PostForm, ReviewForm
# Create your views here.


### Post
class Index(View):
    def get(self, request):
        # print(request.user.username)
        post_objs = Post.objects.all()
        context = {
            'posts':post_objs,
            'title':'Blog'
        }
        
        return render(request, 'blog/post_list.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = Post.objects.prefetch_related('review_set').get(pk=pk)
        reviews = post.review_set.all()
        review_form = ReviewForm()
        context = {
            'title' : 'Blog',
            'post_id' : pk,
            'post_title' : post.title,
            'post_content' : post.content,
            'post_writer' : post.writer,
            'post_created_at' : post.created_at,
            'post_name':post.name,
            'reviews' : reviews,
            'review_form' : review_form
        }
        return render(request, 'blog/post_detail.html', context)


class Write(LoginRequiredMixin, View):
    def get(self, request):
        # print(business_id)
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_form.html', context)
        # else:
        #     return redirect('blog:list')
            
    def post(self, request):
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.name = request.user.name
            post.address = request.user.fulladdress
            post.save()
            return redirect('blog:list')
        
        context = {
            'form':form
        }
        return render(request, 'blog/post_form.html')


class Update(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        
        form = PostForm(initial={'title':post.title, 'content':post.content})
        
        context = {
            'title':'Blog',
            'form':form,
            'post':post
        }
        return render(request, 'blog/post_edit.html', context)
    
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('blog:detail', pk=pk)
        context = {
            'form':form
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
        context = {
            'title': 'Blog',
            'post_id': pk,
            'post_title': reviews[0].post.title,
            'post_content' : reviews[0].post.content,
            'post_writer' : reviews[0].post.writer,
            'post_created_at' : reviews[0].post.created_at,
            'reviews' : post.comment_set.all(),
            'review_form' : form,
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