from rest_framework import serializers
from .models import Category, Tag, Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    categories_ids = serializers.ListField(write_only=True, required=False)
    tags_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'video', 'categories', 'tags', 'categories_ids', 'tags_ids']

    def create(self, validated_data):
        categories_ids = validated_data.pop('categories_ids', [])
        tags_ids = validated_data.pop('tags_ids', [])
        post = Post.objects.create(**validated_data)
        post.categories.set(categories_ids)
        post.tags.set(tags_ids)
        return post

    def update(self, instance, validated_data):
        categories_ids = validated_data.pop('categories_ids', [])
        tags_ids = validated_data.pop('tags_ids', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.video = validated_data.get('video', instance.video)
        instance.save()
        instance.categories.set(categories_ids)
        instance.tags.set(tags_ids)
        return instance