from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class for blog posts and other models"""
    page_size = 10  
    page_size_query_param = "page_size" 
    max_page_size = 50  
