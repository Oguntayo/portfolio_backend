from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db.models import Avg

User = get_user_model()

class Project(models.Model):
    """Project model to showcase portfolio work"""
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    technologies = models.JSONField(default=list)  # Store list of tech stacks
    repository_link = models.URLField()
    live_demo = models.URLField(blank=True, null=True)
    tags = models.JSONField(default=list)  # Categories (AI, Web App, etc.)
    completion_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    claps = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def average_rating(self):
        """Calculate the average rating of the project"""
        return self.reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    def review_count(self):
        """Get the total number of reviews"""
        return self.reviews.count()

    class Meta:
        ordering = ["-created_at"]

class ProjectImage(models.Model):
    """Model for storing multiple images for a project"""
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="project_images/")

    def __str__(self):
        return f"Image for {self.project.title}"


class Review(models.Model):
    """Model for project reviews/testimonials"""
    project = models.ForeignKey(Project, related_name="reviews", on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # Show newest reviews first

    def __str__(self):
        return f"Review by {self.reviewer} on {self.project.title}"
