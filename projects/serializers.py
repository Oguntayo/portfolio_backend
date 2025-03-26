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
    image = serializers.ImageField(write_only=True, required=False)  # Accept image during creation
    image_url = serializers.SerializerMethodField()  # Return image URL

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "technologies", "repository_link",
            "live_demo", "tags", "completion_date", "views", "claps",
            "featured", "image", "image_url"
        ]

    def get_image_url(self, obj):
        """Return the project's first image URL"""
        image = obj.images.first()
        return image.image.url if image else None
    def validate_repository_link(self, value):
        """Ensure repository link is from GitHub, GitLab, or Bitbucket"""
        if not re.match(r"https?://(github\.com|gitlab\.com|bitbucket\.org)/", value):
            raise serializers.ValidationError("Repository link must be a valid GitHub, GitLab, or Bitbucket URL.")
        return value

    def create(self, validated_data):
        """Create a project and handle the image upload"""
        image = validated_data.pop("image", None)
        project = Project.objects.create(**validated_data)

        if image:
            ProjectImage.objects.create(project=project, image=image)

        return project

