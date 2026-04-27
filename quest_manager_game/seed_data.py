"""
Seed script for Quest Manager Game.

Creates initial data for testing:
- 1 Admin user (admin/admin123)
- 2 Player users with characters
- 6 Sample quests of varying difficulty
- Some accepted/completed quests for demo purposes
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quest_manager_game.settings')
django.setup()

from django.contrib.auth.models import User
from game.models import Character, Quest, PlayerQuest

def seed():
    print("=" * 60)
    print("  Seeding Quest Manager Game Database")
    print("=" * 60)

    # -----------------------------------------------------------------
    # Create Admin User
    # -----------------------------------------------------------------
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@questmanager.com',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("[+] Admin user created: admin / admin123")
    else:
        print("[=] Admin user already exists")

    # -----------------------------------------------------------------
    # Create Player Users
    # -----------------------------------------------------------------
    player1, created = User.objects.get_or_create(
        username='player1',
        defaults={'email': 'player1@questmanager.com'}
    )
    if created:
        player1.set_password('player123')
        player1.save()
        print("[+] Player 1 created: player1 / player123")
    else:
        print("[=] Player 1 already exists")

    player2, created = User.objects.get_or_create(
        username='player2',
        defaults={'email': 'player2@questmanager.com'}
    )
    if created:
        player2.set_password('player123')
        player2.save()
        print("[+] Player 2 created: player2 / player123")
    else:
        print("[=] Player 2 already exists")

    # -----------------------------------------------------------------
    # Create Characters
    # -----------------------------------------------------------------
    char1, created = Character.objects.get_or_create(
        user=player1,
        defaults={
            'name': 'Aragorn the Brave',
            'character_class': 'warrior',
            'xp': 150,
        }
    )
    if created:
        print(f"[+] Character created: {char1.name} (Level {char1.level})")
    else:
        print(f"[=] Character already exists: {char1.name}")

    char2, created = Character.objects.get_or_create(
        user=player2,
        defaults={
            'name': 'Gandalf the Wise',
            'character_class': 'mage',
            'xp': 230,
        }
    )
    if created:
        print(f"[+] Character created: {char2.name} (Level {char2.level})")
    else:
        print(f"[=] Character already exists: {char2.name}")

    # -----------------------------------------------------------------
    # Create Quests
    # -----------------------------------------------------------------
    quests_data = [
        {
            'title': 'Gather Herbs in the Forest',
            'description': 'Venture into the Whispering Woods and collect 10 healing herbs. '
                          'Be careful of the wolves that roam at night.',
            'difficulty': 'easy',
        },
        {
            'title': 'Deliver the King\'s Message',
            'description': 'Carry an urgent message from King Aldric to the neighboring kingdom. '
                          'The roads are safe but the journey is long.',
            'difficulty': 'easy',
        },
        {
            'title': 'Clear the Goblin Camp',
            'description': 'A group of goblins has set up camp near the village. '
                          'Defeat their leader and scatter the rest.',
            'difficulty': 'medium',
        },
        {
            'title': 'Escort the Merchant Caravan',
            'description': 'Protect a merchant caravan traveling through bandit territory. '
                          'Ensure all goods arrive safely at the destination.',
            'difficulty': 'medium',
        },
        {
            'title': 'Slay the Dragon of Mount Doom',
            'description': 'The ancient dragon Scorchfang has awakened and threatens the realm. '
                          'Only the bravest heroes dare face this legendary beast.',
            'difficulty': 'hard',
        },
        {
            'title': 'Retrieve the Lost Artifact',
            'description': 'Deep within the Cursed Dungeon lies the Amulet of Eternity. '
                          'Navigate deadly traps and defeat the dungeon boss to claim it.',
            'difficulty': 'hard',
        },
    ]

    created_quests = []
    for quest_data in quests_data:
        quest, created = Quest.objects.get_or_create(
            title=quest_data['title'],
            defaults={
                'description': quest_data['description'],
                'difficulty': quest_data['difficulty'],
                'created_by': admin_user,
                'is_active': True,
            }
        )
        created_quests.append(quest)
        if created:
            print(f"[+] Quest created: {quest.title} ({quest.get_difficulty_display()} - {quest.xp_reward} XP)")
        else:
            print(f"[=] Quest already exists: {quest.title}")

    # -----------------------------------------------------------------
    # Create some PlayerQuest relationships for demo
    # -----------------------------------------------------------------
    # Player 1: completed 2 quests, 1 accepted
    pq1, created = PlayerQuest.objects.get_or_create(
        player=player1,
        quest=created_quests[0],
        defaults={'status': 'completed'}
    )
    if created:
        from django.utils import timezone
        pq1.completed_at = timezone.now()
        pq1.save()
        print(f"[+] Player 1 completed: {created_quests[0].title}")

    pq2, created = PlayerQuest.objects.get_or_create(
        player=player1,
        quest=created_quests[2],
        defaults={'status': 'completed'}
    )
    if created:
        from django.utils import timezone
        pq2.completed_at = timezone.now()
        pq2.save()
        print(f"[+] Player 1 completed: {created_quests[2].title}")

    pq3, created = PlayerQuest.objects.get_or_create(
        player=player1,
        quest=created_quests[4],
        defaults={'status': 'accepted'}
    )
    if created:
        print(f"[+] Player 1 accepted: {created_quests[4].title}")

    # Player 2: completed 1 quest
    pq4, created = PlayerQuest.objects.get_or_create(
        player=player2,
        quest=created_quests[1],
        defaults={'status': 'completed'}
    )
    if created:
        from django.utils import timezone
        pq4.completed_at = timezone.now()
        pq4.save()
        print(f"[+] Player 2 completed: {created_quests[1].title}")

    print()
    print("=" * 60)
    print("  Seeding Complete!")
    print("=" * 60)
    print()
    print("  Test Accounts:")
    print("  +-----------+----------+-----------+")
    print("  | Username  | Password | Role      |")
    print("  +-----------+----------+-----------+")
    print("  | admin     | admin123 | Admin     |")
    print("  | player1   | player123| Player    |")
    print("  | player2   | player123| Player    |")
    print("  +-----------+----------+-----------+")
    print()

if __name__ == '__main__':
    seed()
