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
    images = ProjectImageSerializer(many=True)  # Make it writable for image uploads
    reviews = ReviewSerializer(many=True, read_only=True)  # Nested reviews
    average_rating = serializers.FloatField(read_only=True)  # Read-only field for avg rating
    review_count = serializers.IntegerField(read_only=True)  # Read-only field for total reviews

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "technologies", "repository_link",
            "live_demo", "tags", "completion_date", "views", "claps",
            "featured", "reviews", "average_rating", "review_count", "images",
        ]
        
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        project = Project.objects.create(**validated_data)
        
        # Create ProjectImage instances
        for image_data in images_data:
            ProjectImage.objects.create(project=project, **image_data)
        
        return project
