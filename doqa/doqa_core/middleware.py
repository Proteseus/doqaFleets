from django.shortcuts import redirect
from django.contrib import messages

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if user has an existing session
            if 'session_key' in request.session:
                # If user tries to log in again, deny the request
                if request.path == '/admin/login/?next=/admin/' and request.method == 'POST':
                    messages.error(request, "You are already logged in.")
                    return redirect('home')  # Redirect to home or any other page
        response = self.get_response(request)
        return response

class HideAdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/login/' and not request.user.is_staff:
            return redirect('dashboard')  # Redirect to home or any other page
        response = self.get_response(request)
        return response
