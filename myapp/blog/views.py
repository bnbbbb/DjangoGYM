from django.shortcuts import render, redirect
from django.views import View
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


class Write(View):
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
            # post.writer = request.user
            post.save()
            return redirect('blog:list')
        
        context = {
            'form':form
        }
        return render(request, 'blog/post_form.html')