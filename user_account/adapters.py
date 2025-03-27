from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    """Custom Account Adapter to disable username field"""
    def save_user(self, request, user, form, commit=True):
        user.username = None
        return super().save_user(request, user, form, commit)

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom Social Account Adapter to disable username field"""
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.username = None 
        return user
