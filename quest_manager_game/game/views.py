"""
Views for the Quest Manager Game application.

Implements all the business logic for:
- Authentication (register, login, logout)
- Player features (character CRUD, quest management)
- Admin features (quest CRUD, user management, statistics dashboard)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone

from .models import Character, Quest, PlayerQuest
from .forms import RegisterForm, CharacterForm, QuestForm
from .decorators import admin_required, player_required


# ===========================================================================
# AUTHENTICATION VIEWS
# ===========================================================================

def register_view(request):
    """
    Handle user registration.
    Creates a new user account with secure password hashing (Django built-in).
    Automatically logs in the user after successful registration.
    """
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after registration
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'game/register.html', {'form': form})


def login_view(request):
    """
    Handle user login with Django's built-in authentication.
    Supports session management.
    """
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            # Redirect to the page they were trying to access, or dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'game/login.html')


def logout_view(request):
    """Log out the current user and redirect to login page."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ===========================================================================
# DASHBOARD VIEWS
# ===========================================================================

@login_required
def dashboard_view(request):
    """
    Main dashboard — routes to admin or player dashboard based on role.
    """
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('player_dashboard')


@login_required
@player_required
def player_dashboard_view(request):
    """
    Player dashboard showing character info, active quests, and stats.
    """
    # Get player's character (if exists)
    character = None
    try:
        character = request.user.character
    except Character.DoesNotExist:
        pass

    # Get player's quest statistics
    player_quests = PlayerQuest.objects.filter(player=request.user)
    accepted_quests = player_quests.filter(status='accepted')
    completed_quests = player_quests.filter(status='completed')

    # Get available quests (active quests not yet accepted by this player)
    accepted_quest_ids = player_quests.values_list('quest_id', flat=True)
    available_quests = Quest.objects.filter(is_active=True).exclude(id__in=accepted_quest_ids)[:5]

    context = {
        'character': character,
        'accepted_quests': accepted_quests[:5],
        'completed_quests': completed_quests.count(),
        'total_quests': player_quests.count(),
        'available_quests': available_quests,
    }
    return render(request, 'game/player_dashboard.html', context)


@login_required
@admin_required
def admin_dashboard_view(request):
    """
    Admin dashboard showing game statistics and management overview.
    """
    # Gather statistics for the admin dashboard
    total_users = User.objects.filter(is_staff=False).count()
    total_characters = Character.objects.count()
    total_quests = Quest.objects.count()
    active_quests = Quest.objects.filter(is_active=True).count()
    total_completed = PlayerQuest.objects.filter(status='completed').count()
    total_accepted = PlayerQuest.objects.filter(status='accepted').count()

    # Quest difficulty distribution
    quest_stats = Quest.objects.values('difficulty').annotate(count=Count('id'))

    # Top players by XP
    top_characters = Character.objects.order_by('-xp')[:10]

    # Recent activity
    recent_completions = PlayerQuest.objects.filter(
        status='completed'
    ).select_related('player', 'quest').order_by('-completed_at')[:10]

    context = {
        'total_users': total_users,
        'total_characters': total_characters,
        'total_quests': total_quests,
        'active_quests': active_quests,
        'total_completed': total_completed,
        'total_accepted': total_accepted,
        'quest_stats': quest_stats,
        'top_characters': top_characters,
        'recent_completions': recent_completions,
    }
    return render(request, 'game/admin_dashboard.html', context)


# ===========================================================================
# CHARACTER VIEWS (Player Only)
# ===========================================================================

@login_required
@player_required
def character_view(request):
    """
    Display the player's character details.
    If no character exists, redirect to character creation.
    """
    try:
        character = request.user.character
    except Character.DoesNotExist:
        messages.info(request, "You don't have a character yet. Create one!")
        return redirect('character_create')

    # Get quest history for this player
    quest_history = PlayerQuest.objects.filter(
        player=request.user
    ).select_related('quest').order_by('-accepted_at')

    context = {
        'character': character,
        'quest_history': quest_history,
    }
    return render(request, 'game/character_detail.html', context)


@login_required
@player_required
def character_create_view(request):
    """
    Create a new character for the player.
    Each player can only have one character.
    """
    # Check if player already has a character
    try:
        request.user.character
        messages.warning(request, "You already have a character!")
        return redirect('character_detail')
    except Character.DoesNotExist:
        pass

    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user  # Assign to current user
            character.save()
            messages.success(request, f"Character '{character.name}' created successfully!")
            return redirect('character_detail')
    else:
        form = CharacterForm()

    return render(request, 'game/character_form.html', {
        'form': form,
        'action': 'Create',
    })


@login_required
@player_required
def character_edit_view(request):
    """
    Edit the player's existing character.
    Only the character's name and class can be changed.
    """
    try:
        character = request.user.character
    except Character.DoesNotExist:
        messages.error(request, "You don't have a character to edit.")
        return redirect('character_create')

    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            messages.success(request, "Character updated successfully!")
            return redirect('character_detail')
    else:
        form = CharacterForm(instance=character)

    return render(request, 'game/character_form.html', {
        'form': form,
        'action': 'Edit',
        'character': character,
    })


@login_required
@player_required
def character_delete_view(request):
    """
    Delete the player's character.
    Requires POST confirmation to prevent accidental deletion.
    """
    try:
        character = request.user.character
    except Character.DoesNotExist:
        messages.error(request, "You don't have a character to delete.")
        return redirect('player_dashboard')

    if request.method == 'POST':
        character_name = character.name
        character.delete()
        # Also remove all player quests
        PlayerQuest.objects.filter(player=request.user).delete()
        messages.success(request, f"Character '{character_name}' has been deleted.")
        return redirect('player_dashboard')

    return render(request, 'game/character_confirm_delete.html', {
        'character': character,
    })


# ===========================================================================
# QUEST VIEWS (Player)
# ===========================================================================

@login_required
@player_required
def quest_list_view(request):
    """
    Display all available quests for the player.
    Shows quest status (available, accepted, completed) for each quest.
    """
    # Get all active quests
    quests = Quest.objects.filter(is_active=True)

    # Get player's quest relationships
    player_quest_map = {}
    player_quests = PlayerQuest.objects.filter(player=request.user)
    for pq in player_quests:
        player_quest_map[pq.quest_id] = pq.status

    # Annotate quests with player status
    quest_data = []
    for quest in quests:
        quest_data.append({
            'quest': quest,
            'status': player_quest_map.get(quest.id, 'available'),
        })

    context = {
        'quest_data': quest_data,
    }
    return render(request, 'game/quest_list.html', context)


@login_required
@player_required
def quest_accept_view(request, quest_id):
    """
    Accept a quest. Creates a PlayerQuest record with 'accepted' status.
    Player must have a character to accept quests.
    """
    quest = get_object_or_404(Quest, id=quest_id, is_active=True)

    # Check if player has a character
    try:
        request.user.character
    except Character.DoesNotExist:
        messages.error(request, "You need a character to accept quests!")
        return redirect('character_create')

    # Check if already accepted
    if PlayerQuest.objects.filter(player=request.user, quest=quest).exists():
        messages.warning(request, "You have already accepted this quest.")
        return redirect('quest_list')

    # Accept the quest
    PlayerQuest.objects.create(player=request.user, quest=quest)
    messages.success(request, f"Quest '{quest.title}' accepted!")
    return redirect('quest_list')


@login_required
@player_required
def quest_complete_view(request, quest_id):
    """
    Mark a quest as completed.
    Awards XP to the player's character based on quest difficulty.
    """
    player_quest = get_object_or_404(
        PlayerQuest,
        player=request.user,
        quest_id=quest_id,
        status='accepted'
    )

    if request.method == 'POST':
        success = player_quest.complete_quest()
        if success:
            xp = player_quest.quest.xp_reward
            messages.success(
                request,
                f"Quest '{player_quest.quest.title}' completed! You earned {xp} XP!"
            )
        else:
            messages.error(request, "Could not complete the quest.")
        return redirect('quest_list')

    return render(request, 'game/quest_complete_confirm.html', {
        'player_quest': player_quest,
    })


# ===========================================================================
# QUEST MANAGEMENT VIEWS (Admin Only)
# ===========================================================================

@login_required
@admin_required
def admin_quest_list_view(request):
    """
    Admin view to list all quests with management options.
    """
    quests = Quest.objects.all().select_related('created_by')

    # Count players per quest
    for quest in quests:
        quest.player_count = PlayerQuest.objects.filter(quest=quest).count()
        quest.completed_count = PlayerQuest.objects.filter(
            quest=quest, status='completed'
        ).count()

    return render(request, 'game/admin_quest_list.html', {'quests': quests})


@login_required
@admin_required
def admin_quest_create_view(request):
    """
    Admin view to create a new quest.
    """
    if request.method == 'POST':
        form = QuestForm(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            quest.created_by = request.user  # Set the admin as creator
            quest.save()
            messages.success(request, f"Quest '{quest.title}' created successfully!")
            return redirect('admin_quest_list')
    else:
        form = QuestForm()

    return render(request, 'game/admin_quest_form.html', {
        'form': form,
        'action': 'Create',
    })


@login_required
@admin_required
def admin_quest_edit_view(request, quest_id):
    """
    Admin view to edit an existing quest.
    """
    quest = get_object_or_404(Quest, id=quest_id)

    if request.method == 'POST':
        form = QuestForm(request.POST, instance=quest)
        if form.is_valid():
            form.save()
            messages.success(request, f"Quest '{quest.title}' updated successfully!")
            return redirect('admin_quest_list')
    else:
        form = QuestForm(instance=quest)

    return render(request, 'game/admin_quest_form.html', {
        'form': form,
        'action': 'Edit',
        'quest': quest,
    })


@login_required
@admin_required
def admin_quest_delete_view(request, quest_id):
    """
    Admin view to delete a quest.
    Requires POST confirmation.
    """
    quest = get_object_or_404(Quest, id=quest_id)

    if request.method == 'POST':
        quest_title = quest.title
        quest.delete()
        messages.success(request, f"Quest '{quest_title}' has been deleted.")
        return redirect('admin_quest_list')

    return render(request, 'game/admin_quest_confirm_delete.html', {
        'quest': quest,
    })


# ===========================================================================
# USER MANAGEMENT VIEWS (Admin Only)
# ===========================================================================

@login_required
@admin_required
def admin_user_list_view(request):
    """
    Admin view to list all users with their character info.
    """
    users = User.objects.filter(is_staff=False).select_related('character')

    user_data = []
    for user in users:
        character = None
        try:
            character = user.character
        except Character.DoesNotExist:
            pass

        quest_count = PlayerQuest.objects.filter(player=user).count()
        completed_count = PlayerQuest.objects.filter(
            player=user, status='completed'
        ).count()

        user_data.append({
            'user': user,
            'character': character,
            'quest_count': quest_count,
            'completed_count': completed_count,
        })

    return render(request, 'game/admin_user_list.html', {'user_data': user_data})


@login_required
@admin_required
def admin_user_toggle_view(request, user_id):
    """
    Admin view to activate/deactivate a user account.
    """
    user = get_object_or_404(User, id=user_id, is_staff=False)

    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User '{user.username}' has been {status}.")

    return redirect('admin_user_list')


# ===========================================================================
# HOME / INDEX VIEW
# ===========================================================================

def home_view(request):
    """
    Home page — redirects to dashboard if authenticated, or shows landing page.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'game/home.html')
