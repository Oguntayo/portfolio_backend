from rest_framework import serializers
from .models import Blog, Comment

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    author = serializers.ReadOnlyField(source="author.email")  # Show author email instead of ID
    total_likes = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "parent", "total_likes", "created_at"]  # ❌ Removed `blog`

class BlogSerializer(serializers.ModelSerializer):
    """Serializer for Blog posts"""
    author = serializers.ReadOnlyField(source="author.email")  # Do not expect author to be passed in
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
        validated_data['author'] = self.context['request'].user  # Set the author to the current authenticated user
        return super().create(validated_data)

class LikeSerializer(serializers.Serializer):
    """Serializer for liking/unliking a comment or blog post."""
    success = serializers.BooleanField()
    message = serializers.CharField()
