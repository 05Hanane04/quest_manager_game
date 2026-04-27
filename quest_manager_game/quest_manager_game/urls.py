"""
Main URL configuration for the Quest Manager Game project.

Routes:
- /admin/  -> Django built-in admin interface
- /        -> Game application URLs (authentication, player, admin features)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django built-in admin interface
    path('admin/', admin.site.urls),

    # Game application URLs (includes all game-related routes)
    path('', include('game.urls')),
]
