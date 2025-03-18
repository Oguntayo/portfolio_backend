from django.urls import path
from .views import (
    BlogListCreateView, BlogDetailView, CommentListCreateView, 
    LikeBlogView, LikeCommentView
)

urlpatterns = [
    path("", BlogListCreateView.as_view(), name="blog-list-create"),
    path("<int:pk>/", BlogDetailView.as_view(), name="blog-detail"),
    path("<int:blog_id>/comments/", CommentListCreateView.as_view(), name="blog-comments"),
    path("<int:blog_id>/like/", LikeBlogView.as_view(), name="blog-like"),
    path("comments/<int:comment_id>/like/", LikeCommentView.as_view(), name="comment-like"),
]
