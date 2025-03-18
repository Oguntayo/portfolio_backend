from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.utils.response.response import success, error
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.utils.response.response import success
@api_view(['GET'])
def api_overview(request):
    return success("welcome to portfolio API")


@api_view(['GET'])
def health_check(request):
    """Health check endpoint to verify API status"""
    return success("Portfolio API is up and running!")
