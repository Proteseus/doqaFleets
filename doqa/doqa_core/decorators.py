from django.shortcuts import redirect

def staff_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('dashboard')  # Redirect to home or any other page
        return view_func(request, *args, **kwargs)
    return wrapped_view
