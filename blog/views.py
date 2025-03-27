from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer, LikeSerializer
from .pagination import StandardResultsSetPagination
from api.utils.response.response import success, error

class BlogListCreateView(generics.ListCreateAPIView):
    """List all blogs (paginated) & create new blog posts"""
    queryset = Blog.objects.all().order_by("-created_at").prefetch_related("comments")
    serializer_class = BlogSerializer
    pagination_class = StandardResultsSetPagination  
    parser_classes = [MultiPartParser, FormParser] 

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_context(self):
        """Override to pass request to serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


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
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination  

    def get_queryset(self):
        """Filter comments by blog"""
        blog_id = self.kwargs.get("blog_id")
        return Comment.objects.filter(blog_id=blog_id)

    def perform_create(self, serializer):
        """Add the author if authenticated, else set to None (Anonymous)"""
        blog_id = self.kwargs.get("blog_id")
        blog = get_object_or_404(Blog, id=blog_id)

        author = self.request.user if self.request.user.is_authenticated else None
        serializer.save(blog=blog, author=author)

class LikeCommentView(generics.GenericAPIView):
    """View to like/unlike a comment."""
    serializer_class = LikeSerializer

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user if request.user.is_authenticated else None  

        if user:
            if user in comment.likes.all():
                comment.likes.remove(user)
                message = "Unliked comment"
            else:
                comment.likes.add(user)
                message = "Liked comment"

            return Response({"success": True, "message": message, "total_likes": comment.total_likes()}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": "Login required to like comments."}, status=status.HTTP_401_UNAUTHORIZED)
    

class LikeBlogView(generics.GenericAPIView):
    """View to like/unlike a blog post."""
    serializer_class = LikeSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        user = request.user if request.user.is_authenticated else None

        if user:
            if blog.likes.filter(id=user.id).exists():
                blog.likes.remove(user)
                liked = False
            else:
                blog.likes.add(user)
                liked = True

            return Response({"success": True, "liked": liked, "total_likes": blog.total_likes()}, status=status.HTTP_200_OK)

        return Response({"success": False, "message": "Login required to like blog posts."}, status=status.HTTP_401_UNAUTHORIZED)

class LikeBlogView(generics.GenericAPIView):
    """View to like/unlike a blog post."""
    serializer_class = LikeSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, id=blog_id)
        user = request.user if request.user.is_authenticated else None

        if user:
            if blog.likes.filter(id=user.id).exists():
                blog.likes.remove(user)
                liked = False
            else:
                blog.likes.add(user)
                liked = True
        else:
            session = request.session
            liked_blogs = session.get("liked_blogs", [])

            if blog_id in liked_blogs:
                liked_blogs.remove(blog_id) 
                liked = False
            else:
                liked_blogs.append(blog_id)  
                liked = True

            session["liked_blogs"] = liked_blogs  
            session.modified = True 

        return Response(
            {"success": True, "liked": liked, "total_likes": blog.total_likes(request)},
            status=status.HTTP_200_OK,
        )
