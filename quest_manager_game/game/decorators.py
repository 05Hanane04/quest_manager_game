"""
Custom decorators for role-based access control.

Provides decorators to protect views based on user roles:
- admin_required: Only staff/superuser can access
- player_required: Only non-staff authenticated users can access
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator that restricts access to admin (staff) users only.
    Redirects non-admin users to the dashboard with an error message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def player_required(view_func):
    """
    Decorator that restricts access to player (non-staff) users only.
    Redirects admin users to the admin dashboard.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_staff:
            messages.info(request, "This page is for players only.")
            return redirect('admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
