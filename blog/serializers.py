from rest_framework import serializers
from .models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author = serializers.ReadOnlyField(source="author.email")  # Show author email instead of ID
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ["id", "blog", "author", "content", "parent", "total_likes", "created_at"]


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for Blog posts"""
    author = serializers.ReadOnlyField(source="author.email")
    comments = serializers.SerializerMethodField()
    total_likes = serializers.ReadOnlyField()
    image = serializers.ImageField(required=False)  # ✅ Allow image upload

    class Meta:
        model = Blog
        fields = ["id", "title", "content", "image", "author", "total_likes", "comments", "created_at", "updated_at"]

    def get_comments(self, obj):
        """Retrieve related comments"""
        return CommentSerializer(obj.comments.all(), many=True).data

class LikeSerializer(serializers.Serializer):
    """Serializer for liking/unliking a comment or blog post."""
    success = serializers.BooleanField()
    message = serializers.CharField()
