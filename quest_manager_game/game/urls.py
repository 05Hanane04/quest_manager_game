"""
URL configuration for the Quest Manager Game application.

Defines all URL patterns organized by feature:
- Authentication (login, register, logout)
- Player features (dashboard, character CRUD, quest management)
- Admin features (dashboard, quest CRUD, user management)
"""

from django.urls import path
from . import views

urlpatterns = [
    # ===================================================================
    # HOME
    # ===================================================================
    path('', views.home_view, name='home'),

    # ===================================================================
    # AUTHENTICATION
    # ===================================================================
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # ===================================================================
    # DASHBOARD (routes to player or admin dashboard based on role)
    # ===================================================================
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/player/', views.player_dashboard_view, name='player_dashboard'),
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),

    # ===================================================================
    # CHARACTER (Player Only)
    # ===================================================================
    path('character/', views.character_view, name='character_detail'),
    path('character/create/', views.character_create_view, name='character_create'),
    path('character/edit/', views.character_edit_view, name='character_edit'),
    path('character/delete/', views.character_delete_view, name='character_delete'),

    # ===================================================================
    # QUESTS (Player)
    # ===================================================================
    path('quests/', views.quest_list_view, name='quest_list'),
    path('quests/<int:quest_id>/accept/', views.quest_accept_view, name='quest_accept'),
    path('quests/<int:quest_id>/complete/', views.quest_complete_view, name='quest_complete'),

    # ===================================================================
    # ADMIN - QUEST MANAGEMENT
    # ===================================================================
    path('admin-panel/quests/', views.admin_quest_list_view, name='admin_quest_list'),
    path('admin-panel/quests/create/', views.admin_quest_create_view, name='admin_quest_create'),
    path('admin-panel/quests/<int:quest_id>/edit/', views.admin_quest_edit_view, name='admin_quest_edit'),
    path('admin-panel/quests/<int:quest_id>/delete/', views.admin_quest_delete_view, name='admin_quest_delete'),

    # ===================================================================
    # ADMIN - USER MANAGEMENT
    # ===================================================================
    path('admin-panel/users/', views.admin_user_list_view, name='admin_user_list'),
    path('admin-panel/users/<int:user_id>/toggle/', views.admin_user_toggle_view, name='admin_user_toggle'),
]
