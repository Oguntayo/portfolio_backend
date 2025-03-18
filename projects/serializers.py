from rest_framework import serializers
from .models import Project, ProjectImage, Review
import re


class ProjectImageSerializer(serializers.ModelSerializer):
    """Serializer for handling project images"""

    class Meta:
        model = ProjectImage
        fields = ["id", "image", "project"]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for handling project reviews/testimonials"""
    reviewer = serializers.ReadOnlyField(source="reviewer.email")  # Show reviewer email instead of ID

    class Meta:
        model = Review
        fields = ["id", "reviewer", "comment", "rating", "created_at"]


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model"""
    views = serializers.IntegerField(read_only=True)
    claps = serializers.IntegerField(read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)  # Nested images
    reviews = ReviewSerializer(many=True, read_only=True)  # Nested reviews
    average_rating = serializers.FloatField(read_only=True)  # Read-only field for avg rating
    review_count = serializers.IntegerField(read_only=True)  # Read-only field for total reviews

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "technologies", "repository_link",
            "live_demo", "images", "tags", "completion_date", "views", "claps",
            "featured", "reviews", "average_rating", "review_count",
        ]

    def validate_repository_link(self, value):
        """Ensure repository link is from GitHub, GitLab, or Bitbucket"""
        if not re.match(r"https?://(github\.com|gitlab\.com|bitbucket\.org)/", value):
            raise serializers.ValidationError("Repository link must be a valid GitHub, GitLab, or Bitbucket URL.")
        return value
