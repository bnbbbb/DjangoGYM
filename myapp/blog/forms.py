from django import forms
from .models import Post, Review


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'rows': '3', 'cols': '35'})
        }
        
