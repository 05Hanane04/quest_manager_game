"""
Models for the Quest Manager Game application.

Defines the relational database schema:
- Character: RPG character belonging to a player (one-to-one with User)
- Quest: Quests created by admins with difficulty and XP rewards
- PlayerQuest: Many-to-many relationship between players and quests
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# ---------------------------------------------------------------------------
# Character Model
# ---------------------------------------------------------------------------
class Character(models.Model):
    """
    Represents a player's RPG character.
    Each user (player) can have exactly one character.
    Level is automatically calculated from XP: every 100 XP = +1 level.
    """

    # Character class choices for the RPG system
    CLASS_CHOICES = [
        ('warrior', 'Warrior'),
        ('mage', 'Mage'),
        ('rogue', 'Rogue'),
        ('healer', 'Healer'),
        ('ranger', 'Ranger'),
    ]

    # One-to-one relationship: each user has at most one character
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='character',
        help_text="The player who owns this character"
    )

    # Character attributes
    name = models.CharField(
        max_length=100,
        help_text="The character's display name"
    )
    character_class = models.CharField(
        max_length=20,
        choices=CLASS_CHOICES,
        default='warrior',
        help_text="The character's RPG class"
    )
    xp = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total experience points accumulated"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def level(self):
        """
        Calculate level from XP.
        Every 100 XP = +1 level. Minimum level is 1.
        Example: 230 XP -> Level 3 (floor(230/100) + 1)
        """
        return (self.xp // 100) + 1

    @property
    def xp_for_current_level(self):
        """
        Calculate remaining XP within the current level.
        Example: 230 XP -> 30 XP remaining in current level
        """
        return self.xp % 100

    @property
    def xp_to_next_level(self):
        """
        Calculate XP needed to reach the next level.
        Example: 230 XP -> 70 XP needed for next level
        """
        return 100 - self.xp_for_current_level

    def add_xp(self, amount):
        """
        Add XP to the character and save.
        Args:
            amount (int): The amount of XP to add
        """
        self.xp += amount
        self.save()

    def __str__(self):
        return f"{self.name} (Level {self.level} {self.get_character_class_display()})"

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"
        ordering = ['-xp']


# ---------------------------------------------------------------------------
# Quest Model
# ---------------------------------------------------------------------------
class Quest(models.Model):
    """
    Represents a quest that players can accept and complete.
    Quests are created and managed by admins.
    XP rewards are determined by difficulty level.
    """

    # Difficulty choices with corresponding XP rewards
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),       # 10 XP
        ('medium', 'Medium'),   # 20 XP
        ('hard', 'Hard'),       # 50 XP
    ]

    # XP reward mapping based on difficulty
    XP_REWARDS = {
        'easy': 10,
        'medium': 20,
        'hard': 50,
    }

    # Quest attributes
    title = models.CharField(
        max_length=200,
        help_text="The quest title"
    )
    description = models.TextField(
        help_text="Detailed description of the quest objectives"
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy',
        help_text="Quest difficulty level (determines XP reward)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the quest is currently available"
    )

    # Admin who created the quest
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_quests',
        help_text="Admin who created this quest"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def xp_reward(self):
        """
        Get the XP reward based on quest difficulty.
        Easy -> 10 XP, Medium -> 20 XP, Hard -> 50 XP
        """
        return self.XP_REWARDS.get(self.difficulty, 0)

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()} - {self.xp_reward} XP)"

    class Meta:
        verbose_name = "Quest"
        verbose_name_plural = "Quests"
        ordering = ['-created_at']


# ---------------------------------------------------------------------------
# PlayerQuest Model (Many-to-Many relationship)
# ---------------------------------------------------------------------------
class PlayerQuest(models.Model):
    """
    Represents the relationship between a player and a quest.
    Tracks quest acceptance and completion status.
    When a quest is completed, XP is awarded to the player's character.
    """

    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    ]

    # Foreign keys to create the many-to-many relationship
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='player_quests',
        help_text="The player who accepted this quest"
    )
    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        related_name='player_quests',
        help_text="The quest that was accepted"
    )

    # Quest progress tracking
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='accepted',
        help_text="Current status of the quest for this player"
    )

    # Timestamps
    accepted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the quest was completed"
    )

    def complete_quest(self):
        """
        Mark the quest as completed and award XP to the player's character.
        Only works if the quest hasn't been completed yet.
        Returns True if successful, False otherwise.
        """
        from django.utils import timezone

        if self.status == 'completed':
            return False  # Already completed

        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

        # Award XP to the player's character if they have one
        try:
            character = self.player.character
            character.add_xp(self.quest.xp_reward)
            return True
        except Character.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.player.username} - {self.quest.title} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Player Quest"
        verbose_name_plural = "Player Quests"
        ordering = ['-accepted_at']
        # Ensure a player can only accept a quest once
        unique_together = ['player', 'quest']
