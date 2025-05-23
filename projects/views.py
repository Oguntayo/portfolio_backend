from rest_framework import generics, filters, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.core.exceptions import PermissionDenied
import requests

from .models import Project, Review
from .serializers import ProjectSerializer, ReviewSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    """Handles listing all projects and creating new projects"""
    queryset = Project.objects.all().order_by("-completion_date")
    serializer_class = ProjectSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  


class ProjectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a project"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectViewCountView(APIView):
    """Handles incrementing project view count"""
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.views = F("views") + 1  
        project.save(update_fields=["views"])
        return Response({"message": "View count updated"}, status=status.HTTP_200_OK)


class ProjectClapView(APIView):
    """Handles adding claps to a project"""
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.claps = F("claps") + 1  
        project.save(update_fields=["claps"])
        return Response({"message": "Clap added"}, status=status.HTTP_200_OK)


class GitHubStatsView(APIView):
    """Fetch real-time GitHub stars & forks"""
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        repo_url = project.repository_link
        if "github.com" not in repo_url:
            return Response({"error": "Not a GitHub repository"}, status=status.HTTP_400_BAD_REQUEST)

        repo_path = repo_url.replace("https://github.com/", "")
        api_url = f"https://api.github.com/repos/{repo_path}"
        
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return Response({"stars": data["stargazers_count"], "forks": data["forks_count"]})
        return Response({"error": "Failed to fetch GitHub data"}, status=status.HTTP_400_BAD_REQUEST)



class ReviewListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating reviews for a project"""
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Filter reviews by project ID"""
        return Review.objects.filter(project_id=self.kwargs["project_id"])

    def perform_create(self, serializer):
        """Attach the current user as the reviewer, or set to anonymous"""
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])

        reviewer = self.request.user if self.request.user.is_authenticated else None

        serializer.save(reviewer=reviewer, project=project)
