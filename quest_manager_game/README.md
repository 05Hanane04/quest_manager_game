# Quest Manager Game

A full-featured RPG quest management system built with **Django** and **PostgreSQL**. Players can create characters, accept quests, earn XP, and level up. Admins can manage quests, users, and view statistics.

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Database Schema](#database-schema)
5. [Installation & Setup](#installation--setup)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [Test Accounts](#test-accounts)
9. [XP & Level System](#xp--level-system)
10. [API / URL Routes](#api--url-routes)
11. [Security](#security)
12. [Running Tests](#running-tests)
13. [Screenshots](#screenshots)

---

## Features

### Authentication System
- User registration with form validation
- Secure login/logout with Django's built-in authentication
- Password hashing (PBKDF2 by default)
- Session management with configurable expiration

### Player Features
- Create, view, edit, and delete a character (full CRUD)
- Choose from 5 character classes: Warrior, Mage, Rogue, Healer, Ranger
- View available quests with difficulty and XP rewards
- Accept quests and mark them as completed
- Automatic XP gain and level-up on quest completion
- Personal dashboard with stats and progress bar

### Admin Features
- Statistics dashboard (total players, quests, completions)
- Create, update, and delete quests (full CRUD)
- Define quest difficulty (Easy, Medium, Hard)
- Manage users (activate/deactivate, promote to admin)
- View top players leaderboard
- View recent quest completions

---

## Architecture

The project follows Django's **MTV (Model-Template-View)** architecture:

| Layer | Technology | Description |
|-------|-----------|-------------|
| **Model** | Django ORM + PostgreSQL | Data models with relationships and business logic |
| **Template** | HTML + CSS | Responsive dark-themed RPG UI |
| **View** | Django Views | Request handling, authentication, CRUD operations |

---

## Project Structure

```
quest_manager_game/
├── manage.py                          # Django management script
├── seed_data.py                       # Database seeding script
├── README.md                          # This documentation
│
├── quest_manager_game/                # Project configuration
│   ├── __init__.py
│   ├── settings.py                    # Django settings (DB, apps, middleware)
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI entry point
│   └── asgi.py                        # ASGI entry point
│
├── game/                              # Main application
│   ├── __init__.py
│   ├── models.py                      # Database models (Character, Quest, PlayerQuest)
│   ├── views.py                       # View functions (auth, CRUD, dashboards)
│   ├── urls.py                        # App URL patterns
│   ├── forms.py                       # Django forms (Register, Character, Quest)
│   ├── admin.py                       # Django admin configuration
│   ├── decorators.py                  # Custom role-based access decorators
│   ├── tests.py                       # Unit tests (24 tests)
│   ├── apps.py                        # App configuration
│   └── migrations/                    # Database migrations
│       ├── __init__.py
│       └── 0001_initial.py
│
├── templates/game/                    # HTML templates
│   ├── base.html                      # Base layout with navigation
│   ├── home.html                      # Landing page
│   ├── login.html                     # Login page
│   ├── register.html                  # Registration page
│   ├── player_dashboard.html          # Player dashboard
│   ├── admin_dashboard.html           # Admin dashboard with statistics
│   ├── character_detail.html          # Character detail view
│   ├── character_form.html            # Character create/edit form
│   ├── character_confirm_delete.html  # Character delete confirmation
│   ├── quest_list.html                # Available quests for players
│   ├── quest_complete_confirm.html    # Quest completion confirmation
│   ├── admin_quest_list.html          # Admin quest management
│   ├── admin_quest_form.html          # Admin quest create/edit form
│   ├── admin_quest_confirm_delete.html# Admin quest delete confirmation
│   └── admin_user_list.html           # Admin user management
│
└── static/css/
    └── style.css                      # Main stylesheet (dark RPG theme)
```

---

## Database Schema

The application uses 4 main models with the following relationships:

### Entity-Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│     User     │       │   PlayerQuest    │       │    Quest     │
│ (Django Auth)│       │  (Join Table)    │       │              │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │──1:N──│ id (PK)          │──N:1──│ id (PK)      │
│ username     │       │ player_id (FK)   │       │ title        │
│ password     │       │ quest_id (FK)    │       │ description  │
│ email        │       │ status           │       │ difficulty   │
│ is_staff     │       │ accepted_at      │       │ xp_reward    │
│ ...          │       │ completed_at     │       │ is_active    │
└──────┬───────┘       └──────────────────┘       │ created_by   │
       │                                          │ created_at   │
       │ 1:1                                      └──────────────┘
       │
┌──────┴───────┐
│  Character   │
├──────────────┤
│ id (PK)      │
│ user_id (FK) │
│ name         │
│ character_   │
│   class      │
│ xp           │
│ created_at   │
│ updated_at   │
└──────────────┘
```

### Model Details

| Model | Field | Type | Description |
|-------|-------|------|-------------|
| **Character** | `user` | OneToOneField(User) | Owner of the character |
| | `name` | CharField(100) | Character name |
| | `character_class` | CharField (choices) | warrior, mage, rogue, healer, ranger |
| | `xp` | PositiveIntegerField | Total experience points |
| | `created_at` | DateTimeField | Creation timestamp |
| | `updated_at` | DateTimeField | Last update timestamp |
| **Quest** | `title` | CharField(200) | Quest title |
| | `description` | TextField | Quest description |
| | `difficulty` | CharField (choices) | easy, medium, hard |
| | `xp_reward` | PositiveIntegerField | Auto-calculated from difficulty |
| | `is_active` | BooleanField | Whether quest is available |
| | `created_by` | ForeignKey(User) | Admin who created the quest |
| | `created_at` | DateTimeField | Creation timestamp |
| **PlayerQuest** | `player` | ForeignKey(User) | Player who accepted the quest |
| | `quest` | ForeignKey(Quest) | The accepted quest |
| | `status` | CharField (choices) | accepted, completed |
| | `accepted_at` | DateTimeField | When the quest was accepted |
| | `completed_at` | DateTimeField | When the quest was completed |

---

## Installation & Setup

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install django psycopg2-binary
```

### Step 2: Set Up PostgreSQL

```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE quest_manager_db;"
sudo -u postgres psql -c "CREATE USER quest_admin WITH PASSWORD 'quest_password_2024';"
sudo -u postgres psql -c "ALTER ROLE quest_admin SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE quest_admin SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE quest_admin SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE quest_manager_db TO quest_admin;"
sudo -u postgres psql -c "ALTER DATABASE quest_manager_db OWNER TO quest_admin;"
```

### Step 3: Run Migrations

```bash
cd quest_manager_game
python manage.py makemigrations game
python manage.py migrate
```

### Step 4: Seed the Database (Optional)

```bash
python seed_data.py
```

This creates test accounts and sample data (see [Test Accounts](#test-accounts)).

---

## Configuration

Database configuration is in `quest_manager_game/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quest_manager_db',
        'USER': 'quest_admin',
        'PASSWORD': 'quest_password_2024',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

To use **MySQL** instead, change the engine:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quest_manager_db',
        'USER': 'quest_admin',
        'PASSWORD': 'quest_password_2024',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

And install the MySQL driver: `pip install mysqlclient`

---

## Running the Application

```bash
cd quest_manager_game
python manage.py runserver 0.0.0.0:8000
```

Then open your browser at: **http://localhost:8000/**

---

## Test Accounts

| Username | Password | Role | Character |
|----------|----------|------|-----------|
| `admin` | `admin123` | Admin | — |
| `player1` | `player123` | Player | Aragorn the Brave (Warrior, Level 2) |
| `player2` | `player123` | Player | Gandalf the Wise (Mage, Level 3) |

---

## XP & Level System

### Quest XP Rewards

| Difficulty | XP Reward |
|-----------|-----------|
| Easy | 10 XP |
| Medium | 20 XP |
| Hard | 50 XP |

### Level Calculation

The level system follows a simple formula:

- **Every 100 XP = +1 Level**
- Level = (XP / 100) + 1
- XP remaining in current level = XP % 100

**Examples:**

| Total XP | Level | XP in Current Level | XP to Next Level |
|----------|-------|---------------------|------------------|
| 0 | 1 | 0 | 100 |
| 50 | 1 | 50 | 50 |
| 100 | 2 | 0 | 100 |
| 150 | 2 | 50 | 50 |
| 230 | 3 | 30 | 70 |

---

## API / URL Routes

### Public Routes

| URL | Method | Description |
|-----|--------|-------------|
| `/` | GET | Home / Landing page |
| `/login/` | GET, POST | User login |
| `/register/` | GET, POST | User registration |
| `/logout/` | GET | User logout |

### Player Routes (requires authentication)

| URL | Method | Description |
|-----|--------|-------------|
| `/dashboard/` | GET | Redirect to role-specific dashboard |
| `/dashboard/player/` | GET | Player dashboard |
| `/character/` | GET | View character details |
| `/character/create/` | GET, POST | Create a new character |
| `/character/edit/` | GET, POST | Edit character |
| `/character/delete/` | GET, POST | Delete character |
| `/quests/` | GET | View available quests |
| `/quests/<id>/accept/` | POST | Accept a quest |
| `/quests/<id>/complete/` | GET, POST | Complete a quest |

### Admin Routes (requires admin role)

| URL | Method | Description |
|-----|--------|-------------|
| `/dashboard/admin/` | GET | Admin dashboard with statistics |
| `/admin-panel/quests/` | GET | List all quests |
| `/admin-panel/quests/create/` | GET, POST | Create a new quest |
| `/admin-panel/quests/<id>/edit/` | GET, POST | Edit a quest |
| `/admin-panel/quests/<id>/delete/` | GET, POST | Delete a quest |
| `/admin-panel/users/` | GET | List all users |
| `/admin-panel/users/<id>/toggle-active/` | POST | Toggle user active status |
| `/admin-panel/users/<id>/toggle-staff/` | POST | Toggle user admin status |

---

## Security

The application implements several security measures:

1. **Authentication**: Django's built-in authentication with PBKDF2 password hashing
2. **CSRF Protection**: All POST forms include `{% csrf_token %}`
3. **Role-Based Access Control**: Custom decorators (`@admin_required`, `@player_required`) protect routes
4. **Login Required**: `@login_required` decorator on all protected views
5. **Session Management**: Configurable session expiration (24h by default)
6. **Input Validation**: Django forms handle input validation and sanitization
7. **SQL Injection Prevention**: Django ORM parameterized queries
8. **XSS Protection**: Django template auto-escaping

### Custom Decorators

```python
# Only admins (is_staff=True) can access
@admin_required
def admin_view(request):
    ...

# Only players (is_staff=False) can access
@player_required
def player_view(request):
    ...
```

---

## Running Tests

The project includes 24 unit tests covering models, authentication, and access control:

```bash
python manage.py test game -v 2
```

### Test Coverage

| Test Suite | Tests | Description |
|-----------|-------|-------------|
| `CharacterModelTest` | 8 | Character creation, level calculation, XP system |
| `QuestModelTest` | 1 | Quest XP rewards by difficulty |
| `PlayerQuestModelTest` | 3 | Quest completion, XP award, duplicate prevention |
| `AuthenticationTest` | 6 | Login, register, logout functionality |
| `AccessControlTest` | 6 | Role-based route protection |

**All 24 tests pass successfully.**

---

## Screenshots

### Home Page
The landing page features a dark RPG theme with information about the game mechanics.

### Player Dashboard
Shows character stats (level, XP, progress bar), active quests, and personal statistics.

### Character Detail
Displays full character information, quest history, and XP progress.

### Quest List
Table of all available quests with difficulty badges, XP rewards, and action buttons.

### Admin Dashboard
Statistics overview with total players, quests, completions, leaderboard, and recent activity.

---

## Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11 | Programming language |
| Django | 5.x | Web framework (MTV architecture) |
| PostgreSQL | 14 | Relational database |
| HTML5 | — | Page structure |
| CSS3 | — | Styling (dark RPG theme) |
| Django ORM | — | Database abstraction layer |
| Django Auth | — | Authentication system |

---

## License

This project is created for educational purposes as an RPG quest management system prototype.
