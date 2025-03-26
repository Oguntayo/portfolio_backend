from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Project, Review
from .serializers import ProjectSerializer, ReviewSerializer
import requests


class ProjectListCreateView(generics.ListCreateAPIView):
    """Handles listing all projects and creating new projects"""
    queryset = Project.objects.all().order_by("-completion_date")  # Latest first
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "technologies", "tags"]  # Enable search

    def get_queryset(self):
        """Allow filtering by tag or technology used"""
        queryset = super().get_queryset()
        tag = self.request.query_params.get("tag")
        tech = self.request.query_params.get("tech")

        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        if tech:
            queryset = queryset.filter(technologies__icontains=tech)

        return queryset


class ProjectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting a project"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectViewCountView(APIView):
    """Handles incrementing project view count"""
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.views = F("views") + 1  # Increment views count
        project.save(update_fields=["views"])
        return Response({"message": "View count updated"}, status=status.HTTP_200_OK)


class ProjectClapView(APIView):
    """Handles adding claps to a project"""
    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.claps = F("claps") + 1  # Increment claps
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


from rest_framework.permissions import IsAuthenticated

class ReviewListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating reviews for a project"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def get_queryset(self):
        """Filter reviews by project ID"""
        return Review.objects.filter(project_id=self.kwargs["project_id"])

    def perform_create(self, serializer):
        """Attach the current user as the reviewer"""
        if self.request.user.is_authenticated:  # Ensure the user is authenticated
            print("======",self.request.user)
            project = get_object_or_404(Project, pk=self.kwargs["project_id"])
            serializer.save(reviewer=self.request.user, project=project)
        else:
            raise PermissionDenied("You must be logged in to submit a review.")
