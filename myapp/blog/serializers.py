from rest_framework import serializers
from .models import Post, Tag, PostImage

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields= '__all__'


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
