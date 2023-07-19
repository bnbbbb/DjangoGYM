from django import forms
from .models import Post, Review, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'rows': '3', 'cols': '35'})
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class SearchForm(forms.ModelForm):
    search = forms.CharField(max_length=30)
    class Meta:
        fields = ['search']