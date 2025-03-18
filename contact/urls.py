from django.urls import path
from .views import (
    ContactMessageCreateView, ContactMessageListView, ContactMessageRetrieveView,
    ContactMessageUpdateView, ContactMessagePartialUpdateView, ContactMessageDeleteView
)

urlpatterns = [
    path("contact/", ContactMessageCreateView.as_view(), name="contact-create"),
    path("contact/messages/", ContactMessageListView.as_view(), name="contact-list"),
    path("contact/messages/<int:pk>/", ContactMessageRetrieveView.as_view(), name="contact-retrieve"),
    path("contact/messages/<int:pk>/update/", ContactMessageUpdateView.as_view(), name="contact-update"),
    path("contact/messages/<int:pk>/partial-update/", ContactMessagePartialUpdateView.as_view(), name="contact-partial-update"),
    path("contact/messages/<int:pk>/delete/", ContactMessageDeleteView.as_view(), name="contact-delete"),
]
