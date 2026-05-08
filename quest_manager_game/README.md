# Quest Manager Game 🎮

Un jeu RPG web développé avec Django et MySQL. Les joueurs créent des personnages, acceptent des quêtes et gagnent de l'expérience pour monter de niveau.

---

## Technologies utilisées

- Python 3.14
- Django 6.0.4
- MySQL (via XAMPP)
- mysqlclient 2.2.8
- Bootstrap 5.3.8
- HTML / CSS / JavaScript

---

### Joueur
- Inscription et connexion
- Création et gestion de son personnage (classe, XP, niveau)
- Consulter les quêtes disponibles
- Accepter et compléter des quêtes
- Gagner de l'XP automatiquement à la complétion

### Administrateur
- Créer, modifier et supprimer des quêtes
- Gérer les utilisateurs
- Consulter les statistiques globales du jeu
- Accès au panel admin `/admin-panel/`

---

## Installation et configuration

### Prérequis
- Python 3.x installé
- XAMPP installé avec MySQL démarré

### Étapes

**1. Cloner le projet**
```bash
git clone https://github.com/ton-username/quest-manager-game.git
cd quest-manager-game
```

**2. Créer et activer l'environnement virtuel**
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate
```

**3. Installer les dépendances**
```bash
pip install django mysqlclient
```

**4. Créer la base de données**

Ouvre phpMyAdmin sur `http://localhost/phpmyadmin` et crée une base de données nommée `quest_manager` avec la collation `utf8mb4_unicode_ci`.

**5. Configurer `settings.py`**

Dans `quest_manager_game/settings.py`, modifie le bloc `DATABASES` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quest_manager',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',  # ou 3307 selon ta config XAMPP
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

**6. Appliquer les migrations**
```bash
cd quest_manager_game
python manage.py migrate
```

**7. Insérer les données de test**
```bash
python seed_data.py
```

**8. Lancer le serveur**
```bash
python manage.py runserver
```

L'application est accessible sur `http://127.0.0.1:8000`

---

## Comptes de test

| Rôle | Username | Mot de passe |
|------|----------|--------------|
| Administrateur | admin | admin123 |
| Joueur 1 | player1 | player123 |
| Joueur 2 | player2 | player123 |

---

## Modèles de données

| Modèle | Table MySQL | Description |
|--------|-------------|-------------|
| Character | game_character | Personnage du joueur (nom, classe, XP, niveau) |
| Quest | game_quest | Quêtes créées par l'admin (titre, difficulté, récompense XP) |
| PlayerQuest | game_playerquest | Liaison joueur ↔ quête (statut : accepted / completed) |

---

## Règles de jeu

- Le niveau est calculé automatiquement : `niveau = XP // 100 + 1`
- Récompenses XP : Facile → 10 XP / Moyen → 20 XP / Difficile → 50 XP
- Un joueur ne peut accepter la même quête qu'une seule fois

---

## Auteurs

- **CHALLAL Hanane**
- **TAOUIL Khadija**

Projet réalisé dans le cadre du cours de Programmation Python et Framework — EMSI — 2025/2026