"""
Admin configuration for the Quest Manager Game.

Registers all models with the Django admin site and customizes
the admin interface for better usability.
"""

from django.contrib import admin
from .models import Character, Quest, PlayerQuest


# ---------------------------------------------------------------------------
# Character Admin
# ---------------------------------------------------------------------------
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Admin interface for Character model."""
    list_display = ('name', 'user', 'character_class', 'xp', 'level', 'created_at')
    list_filter = ('character_class',)
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def level(self, obj):
        return obj.level
    level.short_description = 'Level'


# ---------------------------------------------------------------------------
# Quest Admin
# ---------------------------------------------------------------------------
@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    """Admin interface for Quest model."""
    list_display = ('title', 'difficulty', 'xp_reward', 'is_active', 'created_by', 'created_at')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def xp_reward(self, obj):
        return obj.xp_reward
    xp_reward.short_description = 'XP Reward'


# ---------------------------------------------------------------------------
# PlayerQuest Admin
# ---------------------------------------------------------------------------
@admin.register(PlayerQuest)
class PlayerQuestAdmin(admin.ModelAdmin):
    """Admin interface for PlayerQuest model."""
    list_display = ('player', 'quest', 'status', 'accepted_at', 'completed_at')
    list_filter = ('status',)
    search_fields = ('player__username', 'quest__title')
    readonly_fields = ('accepted_at', 'completed_at')
