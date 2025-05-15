from django.urls import path
from .views import RegisterView, LoginView,LogoutView,ProfileView
from django.urls import path
from django.http import HttpResponse

def dummy_signup_view(request):
    return HttpResponse("Signup not allowed.", status=403)

urlpatterns = [
    path("accounts/social/signup/", dummy_signup_view, name="socialaccount_signup"),  
]

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path("profile/", ProfileView.as_view(), name="account-profile"),
    path("accounts/social/signup/", dummy_signup_view, name="socialaccount_signup"),
]