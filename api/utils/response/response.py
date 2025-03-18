from rest_framework.response import Response

def success(message="success",data=None,status_code=200):
    """
    Standardized success response.
    - message: Success message (default "Success")
    - data: Response payload (default `{}`)
    - status_code: HTTP status code (default 200)
    """
    return Response({
        "status":"success",
        "status_code":status_code,
        "message":message,
        "data":data or {}
    },status=status_code)
    
    
def error(message="An error occurred",errors=None,status_code=400):
    """
    Standardized error response.
    - message: Error message (default "An error occurred")
    - errors: Additional error details (default `{}`)
    - status_code: HTTP status code (default 400)
    """
    return Response({
        "status":"error",
        "status_code":status_code,
        "message":message,
        "data":errors or {}
    },status=status_code)