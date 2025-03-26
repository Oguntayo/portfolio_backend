from django.urls import path
from .views import (
    ProjectListCreateView, ProjectRetrieveUpdateDeleteView, 
    ProjectViewCountView, ProjectClapView, GitHubStatsView, ReviewListCreateView
)

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path("<int:pk>", ProjectRetrieveUpdateDeleteView.as_view(), name="project-detail"),
    path("<int:pk>/view", ProjectViewCountView.as_view(), name="project-view-count"),
    path("<int:pk>/clap", ProjectClapView.as_view(), name="project-clap"),
    path("<int:pk>/github-stats", GitHubStatsView.as_view(), name="github-stats"),
    path("<int:project_id>/reviews", ReviewListCreateView.as_view(), name="project-reviews"),
]
