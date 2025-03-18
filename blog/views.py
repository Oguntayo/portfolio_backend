from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from .pagination import StandardResultsSetPagination
from api.utils.response.response import success, error
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BlogListCreateView(generics.ListCreateAPIView):
    """List all blogs (paginated) & create new blog posts"""
    queryset = Blog.objects.all().order_by("-created_at").prefetch_related("comments")
    serializer_class = BlogSerializer
    pagination_class = StandardResultsSetPagination  

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return []

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View, update, or delete a blog post"""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You can only edit your own posts")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("You can only delete your own posts")
        instance.delete()

class CommentListCreateView(generics.ListCreateAPIView):
    """List all comments for a blog post & create new comments"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination  # ✅ Paginate comments

    def get_queryset(self):
        """Filter comments by blog"""
        blog_id = self.kwargs.get("blog_id")
        return Comment.objects.filter(blog_id=blog_id)
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import LikeSerializer
from .models import Comment, Blog

class LikeCommentView(generics.GenericAPIView):
    """View to like/unlike a comment."""
    serializer_class = LikeSerializer  # ✅ Fix Swagger Error

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
            message = "Unliked comment"
        else:
            comment.liked_by.add(user)
            message = "Liked comment"

        return Response({"success": True, "message": message}, status=status.HTTP_200_OK)

class LikeBlogView(generics.GenericAPIView):
    """View to like/unlike a blog post."""
    serializer_class = LikeSerializer  # ✅ Fix Swagger Error

    def post(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        user = request.user
        if user in blog.liked_by.all():
            blog.liked_by.remove(user)
            message = "Unliked blog post"
        else:
            blog.liked_by.add(user)
            message = "Liked blog post"

        return Response({"success": True, "message": message}, status=status.HTTP_200_OK)
