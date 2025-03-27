from rest_framework import serializers
from .models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author = serializers.ReadOnlyField(source="author.email")  
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "parent", "total_likes", "created_at"] 

class BlogSerializer(serializers.ModelSerializer):
    """Serializer for Blog posts"""
    author = serializers.ReadOnlyField(source="author.email")  
    comments = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Blog
        fields = ["id", "title", "content", "image", "author", "total_likes", "comments", "created_at", "updated_at"]

    def get_comments(self, obj):
        """Retrieve related comments"""
        return CommentSerializer(obj.comments.all(), many=True).data

    def create(self, validated_data):
        """Override create method to assign the current user as author"""
        validated_data['author'] = self.context['request'].user  
        return super().create(validated_data)

class LikeSerializer(serializers.Serializer):
    """Serializer for liking/unliking a blog post."""
    success = serializers.BooleanField()
    liked = serializers.BooleanField()
    total_likes = serializers.IntegerField()
