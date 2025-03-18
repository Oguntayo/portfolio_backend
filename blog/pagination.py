from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class for blog posts and other models"""
    page_size = 10  # Default items per page
    page_size_query_param = "page_size"  # Allow client to request custom page size
    max_page_size = 50  # Prevent abuse by setting a max limit
