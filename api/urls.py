from django.urls import path
from api import views
from django.urls import path
from .views import health_check


urlpatterns = [
    path('',views.api_overview,name="api-overview"),
    path("health-check/", health_check, name="health-check"),

]