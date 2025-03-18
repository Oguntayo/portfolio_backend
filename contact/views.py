from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageCreateView(generics.CreateAPIView):
    """Handles creating contact messages"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        """Override create to return a custom success message"""
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Your message has been sent successfully!"},
            status=status.HTTP_201_CREATED
        )

class ContactMessageListView(generics.ListAPIView):
    """Admin-only view to list all contact messages"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]  # Only admin can view all messages

class ContactMessageRetrieveView(generics.RetrieveAPIView):
    """Admin-only view to retrieve a single contact message"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]

class ContactMessageUpdateView(generics.UpdateAPIView):
    """Admin-only view to update a contact message"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]

class ContactMessagePartialUpdateView(generics.UpdateAPIView):
    """Admin-only view to partially update a contact message"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]

class ContactMessageDeleteView(generics.DestroyAPIView):
    """Admin-only view to delete a contact message"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAdminUser]
