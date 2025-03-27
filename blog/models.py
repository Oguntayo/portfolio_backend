from django.db import models
from django.conf import settings

class Blog(models.Model):
    """Blog model to store posts with images"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blogs")
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_blogs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_likes(self, request=None):
        """Returns total number of likes including session-based likes"""
        user_likes_count = self.likes.count()

        session_likes_count = 0
        if request:
            session_likes = request.session.get("liked_blogs", [])
            if self.id in session_likes:
                session_likes_count = 1  

        return user_likes_count + session_likes_count

class Comment(models.Model):
    """Comment model for blog posts"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_comments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"] 

    def __str__(self):
        return f"Comment by {self.author.email} on {self.blog.title}"

    def total_likes(self):
        """Returns total number of likes"""
        return self.likes.count()
