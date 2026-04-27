"""
Tests for the Quest Manager Game application.

Tests cover:
- Model creation and properties
- Level/XP calculation system
- Authentication (login, register, logout)
- Role-based access control
- Character CRUD operations
- Quest acceptance and completion
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Character, Quest, PlayerQuest


# ===========================================================================
# MODEL TESTS
# ===========================================================================

class CharacterModelTest(TestCase):
    """Tests for the Character model."""

    def setUp(self):
        """Create a test user and character."""
        self.user = User.objects.create_user(
            username='testplayer',
            password='testpass123'
        )
        self.character = Character.objects.create(
            user=self.user,
            name='Test Hero',
            character_class='warrior',
            xp=0
        )

    def test_character_creation(self):
        """Test that a character is created correctly."""
        self.assertEqual(self.character.name, 'Test Hero')
        self.assertEqual(self.character.character_class, 'warrior')
        self.assertEqual(self.character.xp, 0)

    def test_level_calculation_base(self):
        """Test level 1 at 0 XP."""
        self.assertEqual(self.character.level, 1)

    def test_level_calculation_230xp(self):
        """Test: 230 XP -> Level 3."""
        self.character.xp = 230
        self.assertEqual(self.character.level, 3)

    def test_xp_for_current_level(self):
        """Test: 230 XP -> 30 XP remaining in current level."""
        self.character.xp = 230
        self.assertEqual(self.character.xp_for_current_level, 30)

    def test_xp_to_next_level(self):
        """Test: 230 XP -> 70 XP to next level."""
        self.character.xp = 230
        self.assertEqual(self.character.xp_to_next_level, 70)

    def test_add_xp(self):
        """Test adding XP to character."""
        self.character.add_xp(50)
        self.assertEqual(self.character.xp, 50)
        self.character.add_xp(60)
        self.assertEqual(self.character.xp, 110)
        self.assertEqual(self.character.level, 2)

    def test_level_at_exact_100(self):
        """Test: 100 XP -> Level 2."""
        self.character.xp = 100
        self.assertEqual(self.character.level, 2)
        self.assertEqual(self.character.xp_for_current_level, 0)

    def test_string_representation(self):
        """Test character __str__ method."""
        self.assertIn('Test Hero', str(self.character))


class QuestModelTest(TestCase):
    """Tests for the Quest model."""

    def test_quest_xp_rewards(self):
        """Test XP rewards for each difficulty level."""
        easy_quest = Quest.objects.create(
            title='Easy Quest', description='Test', difficulty='easy'
        )
        medium_quest = Quest.objects.create(
            title='Medium Quest', description='Test', difficulty='medium'
        )
        hard_quest = Quest.objects.create(
            title='Hard Quest', description='Test', difficulty='hard'
        )

        self.assertEqual(easy_quest.xp_reward, 10)
        self.assertEqual(medium_quest.xp_reward, 20)
        self.assertEqual(hard_quest.xp_reward, 50)


class PlayerQuestModelTest(TestCase):
    """Tests for the PlayerQuest model."""

    def setUp(self):
        """Create test data."""
        self.user = User.objects.create_user(
            username='testplayer', password='testpass123'
        )
        self.character = Character.objects.create(
            user=self.user, name='Hero', character_class='mage', xp=0
        )
        self.quest = Quest.objects.create(
            title='Test Quest', description='A test quest', difficulty='medium'
        )

    def test_complete_quest_awards_xp(self):
        """Test that completing a quest awards XP to the character."""
        pq = PlayerQuest.objects.create(
            player=self.user, quest=self.quest
        )
        result = pq.complete_quest()
        self.assertTrue(result)
        self.assertEqual(pq.status, 'completed')
        self.assertIsNotNone(pq.completed_at)

        # Refresh character from DB
        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 20)  # Medium quest = 20 XP

    def test_cannot_complete_twice(self):
        """Test that a quest cannot be completed twice."""
        pq = PlayerQuest.objects.create(
            player=self.user, quest=self.quest
        )
        pq.complete_quest()
        result = pq.complete_quest()
        self.assertFalse(result)

        self.character.refresh_from_db()
        self.assertEqual(self.character.xp, 20)  # Only 20 XP, not 40

    def test_unique_together(self):
        """Test that a player can only accept a quest once."""
        PlayerQuest.objects.create(player=self.user, quest=self.quest)
        with self.assertRaises(Exception):
            PlayerQuest.objects.create(player=self.user, quest=self.quest)


# ===========================================================================
# AUTHENTICATION TESTS
# ===========================================================================

class AuthenticationTest(TestCase):
    """Tests for authentication views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_login_page_loads(self):
        """Test that login page loads correctly."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        """Test that register page loads correctly."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Test successful login redirects to dashboard."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_failure(self):
        """Test failed login shows error."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        """Test successful registration."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout(self):
        """Test logout redirects to login."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


# ===========================================================================
# ACCESS CONTROL TESTS
# ===========================================================================

class AccessControlTest(TestCase):
    """Tests for role-based access control."""

    def setUp(self):
        self.client = Client()
        self.player = User.objects.create_user(
            username='player', password='pass123'
        )
        self.admin = User.objects.create_user(
            username='admin', password='pass123', is_staff=True
        )

    def test_unauthenticated_redirect(self):
        """Test that unauthenticated users are redirected to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_player_cannot_access_admin_dashboard(self):
        """Test that players cannot access admin dashboard."""
        self.client.login(username='player', password='pass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_cannot_access_player_dashboard(self):
        """Test that admins cannot access player dashboard."""
        self.client.login(username='admin', password='pass123')
        response = self.client.get(reverse('player_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_player_can_access_quest_list(self):
        """Test that players can access quest list."""
        self.client.login(username='player', password='pass123')
        response = self.client.get(reverse('quest_list'))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_admin_quest_list(self):
        """Test that admins can access admin quest list."""
        self.client.login(username='admin', password='pass123')
        response = self.client.get(reverse('admin_quest_list'))
        self.assertEqual(response.status_code, 200)

    def test_player_cannot_create_quest(self):
        """Test that players cannot create quests."""
        self.client.login(username='player', password='pass123')
        response = self.client.get(reverse('admin_quest_create'))
        self.assertEqual(response.status_code, 302)
