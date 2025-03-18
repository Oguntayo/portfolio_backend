from django.urls import path
from .views import (
    ProjectListCreateView, ProjectRetrieveUpdateDeleteView, 
    ProjectViewCountView, ProjectClapView, GitHubStatsView, ReviewListCreateView
)

urlpatterns = [
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("projects/<int:pk>/", ProjectRetrieveUpdateDeleteView.as_view(), name="project-detail"),
    path("projects/<int:pk>/view/", ProjectViewCountView.as_view(), name="project-view-count"),
    path("projects/<int:pk>/clap/", ProjectClapView.as_view(), name="project-clap"),
    path("projects/<int:pk>/github-stats/", GitHubStatsView.as_view(), name="github-stats"),
    path("projects/<int:project_id>/reviews/", ReviewListCreateView.as_view(), name="project-reviews"),
]
