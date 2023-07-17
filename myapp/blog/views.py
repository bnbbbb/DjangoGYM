from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
# Create your views here.


### Post
class Index(View):
    def get(self, request):
        post_objs = Post.objects.all()
        context = {
            'posts':post_objs,
            'title':'Blog'
        }
        
        return render(request, 'blog/post_list.html', context)


class DetailView(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        
        context = {
            'post':post,
        }
        return render(request, 'blog/post_detail.html', context)


class Write(LoginRequiredMixin, View):
    def get(self, request):
        form  = PostForm()
        context = {
            'form' :form,
        }
        return render(request, 'blog/post_form.html', context)
    def post(self, request):
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.name = request.user.name
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