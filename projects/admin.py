from django.contrib import admin
from .models import Project, ProjectImage, Review

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "completion_date", "featured", "average_rating", "review_count")
    search_fields = ("title", "description", "technologies", "tags")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("featured", "completion_date")
    ordering = ("-created_at",)

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "uploaded_at")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("project", "reviewer", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("project__title", "reviewer__username", "comment")

