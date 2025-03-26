from django.contrib import admin
from .models import Blog, Comment

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "total_likes")
    search_fields = ("title", "author__email")
    list_filter = ("created_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("blog", "author", "created_at", "total_likes")
    search_fields = ("blog__title", "author__email", "content")
    list_filter = ("created_at",)

