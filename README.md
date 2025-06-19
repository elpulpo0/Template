### Template

## Structure

```sh
template/
├── backend/                                   # Code backend de l'application (API, logique serveur)
│   ├── Dockerfile                             # Dockerfile pour construire l'image backend
│   ├── database/                              # Fichiers db générés
│   ├── logs/                                  # Fichiers de logs (erreurs, debug, info)
│   ├── modules/                               # Modules Python principaux
│   │   ├── api/                               # API REST (FastAPI, routes, schémas...)
│   │   │   ├── auth/                          # Authentification (routes, modèles, sécurité)
│   │   │   │   ├── functions.py
│   │   │   │   ├── models.py
│   │   │   │   ├── routes.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── security.py
│   │   │   ├── main.py                        # Point d'entrée FastAPI backend
│   │   │   └── users/                         # Gestion utilisateurs (modèles, routes...)
│   │   │       ├── create_db.py
│   │   │       ├── functions.py
│   │   │       ├── initial_users.yaml         # Données utilisateurs initiales
│   │   │       ├── initial_users.yaml.example # Exemple de fichier utilisateurs
│   │   │       ├── models.py
│   │   │       ├── routes.py
│   │   │       └── schemas.py
│   │   └── database/                          # Configuration et session de la base de données
│   │       ├── config.py
│   │       ├── dependencies.py
│   │       └── session.py
│   ├── requirements.txt                       # Dépendances Python du backend
│   └── utils/
│       └── logger_config.py                   # Configuration du logger
├── bonus_scripts/                             # Scripts utilitaires pour dev ou gestion
│   ├── generate_secret_key.py                 # Script pour générer une clé secrète (ex: JWT)
│   └── print_tree.py                          # Script pour afficher l’arborescence du projet
├── docker-compose.yml                         # Orchestration Docker (backend + frontend)
├── frontend/                                  # Code frontend de l’application (Vue.js)
│   ├── Dockerfile                             # Dockerfile pour construire l’image frontend
│   ├── index.html                             # Page HTML principale
│   ├── package.json                           # Dépendances et scripts frontend (npm)
│   ├── public/                                # Fichiers publics (favicon, assets statiques)
│   └── src/                                   # Code source Vue.js
│       ├── App.vue                            # Composant racine Vue
│       ├── assets/                            # Images, logos, styles globaux
│       │   └── logo.png
│       ├── components/                        # Composants Vue réutilisables
│       │   ├── Auth.vue
│       │   └── Footer.vue
│       ├── functions/                         # Fonctions utilitaires frontend (TS)
│       │   └── utils.ts
│       ├── main.ts                            # Point d’entrée frontend Vue
│       ├── pages/                             # Pages Vue (ex: Users.vue)
│       │   └── Users.vue
│       ├── router/                            # Gestion des routes Vue Router
│       │   └── index.ts
│       ├── stores/                            # Stockage état global (Pinia)
│       │   └── useAuthStore.ts
│       └── styles/                            # Fichiers CSS / styles globaux
│           └── styles.css
├── run_backend.py                             # Script pour lancer le backend (dev local)
└── run_frontend.py                            # Script pour lancer le frontend (dev local)
```

## Installation

**Clone this repository**

```sh
git clone https://github.com/Microphyt/Template.git
```

**Create and edit your environnement file**

```sh
cp .env.example .env
```

```
SECRET_KEY=     # Generate a new secret key with this script : bonus_scripts\generate_secret_key.py
GITHUB_URL=     # The address of your git repository
APP_NAME=       # The name of your application
PORT_BACK=      # The port you want to use for the backend of your application
PORT_FRONT=     # The port you want to use for the frontend of your application
```

**Create and edit your initial users config file**

```sh
cp backend/modules/api/users/initial_users.yaml.example backend/modules/api/users/initial_users.yaml
```

**Launch with Docker**

```sh
docker compose up -d --build
```

## Available services with Docker Compose

- **FastAPI** → http://localhost:{PORT_BACK}
- **Prefect UI** → http://localhost:4200
- **Uptime Kuma** → http://localhost:3001
- **Frontend** → http://localhost:{PORT_FRONT}

**Configure Kuma**

Visit http://localhost:3001 et add the API health check : http://api:{PORT_BACK}/health and a notification through Discord or Telegram.

**Launch in local mode**

Open 2 different terminals:

# Backend (in terminal 1)

```sh
cd backend
```

**Create a virtual environnement**

```sh
python -m venv .venv
```

**Connect to the virtual environnement**

```sh
source .venv/Scripts/activate
```

**Upgrade pip and install librairies**

```sh
python.exe -m pip install --upgrade pip
```

```sh
pip install -r requirements.txt
```

**Run the app**

```sh
cd ../ && python run_backend.py
```

# Frontend (in terminal 2)

```sh
cd frontend
```

**Install dependencies**

```sh
npm install
```

**Run the app**

```sh
cd ../ && python run_frontend.py
```

