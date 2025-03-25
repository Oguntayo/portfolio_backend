"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from user_account.views import GoogleLoginView  

def home(request):
    html_content = """
    <html>
        <head>
            <title>Welcome | Portfolio API</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
                h1 { color: #2c3e50; }
                p { font-size: 18px; }
                a { color: #3498db; text-decoration: none; font-weight: bold; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>Welcome to My Portfolio API</h1>
            <p>Explore my API <a href='/swagger/'>here</a> 🚀</p>
        </body>
    </html>
    """
    return HttpResponse(html_content)

schema_view = get_schema_view(
    openapi.Info(
        title="Portfolio API",
        default_version = "v1",
        description = "API documentation for portfolio",
    ),
    public=True,
    permission_classes=(AllowAny,),
)
urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("account/", include("user_account.urls")), 
    path("blog/", include("blog.urls")), 
    path("projects/", include("projects.urls")), 
    path("contact/", include("contact.urls")), 
    path("google/login/", GoogleLoginView.as_view(), name="google-login"),


    path("accounts/google/login/", oauth2_login, name="google_login"),
    path("accounts/google/login/callback/", oauth2_callback, name="google_callback"),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
