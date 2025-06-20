### Template

## Structure

```sh
template/
# Authentication part
├── auth/                                      # Backend code for authentication management (API, server logic)
│   ├── Dockerfile                             # Dockerfile to build the auth image
│   ├── database/                              # Generated database files
│   ├── logs/                                  # Log files (errors, debug, info)
│   ├── tests/                                 # Test files (pytest)
│   ├── modules/                               # Main Python modules
│   │   ├── api/                               # REST API (FastAPI, routes, schemas...)
│   │   │   ├── auth/                          # Authentication (routes, models, security)
│   │   │   │   ├── functions.py
│   │   │   │   ├── models.py
│   │   │   │   ├── routes.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── security.py
│   │   │   ├── main.py                        # FastAPI entry point
│   │   │   ├── requirements.txt              # Python dependencies
│   │   │   └── users/                         # User management (models, routes...)
│   │   │       ├── create_db.py
│   │   │       ├── functions.py
│   │   │       ├── initial_users.yaml         # Initial user data
│   │   │       ├── initial_users.yaml.example # Example user file
│   │   │       ├── models.py
│   │   │       ├── routes.py
│   │   │       └── schemas.py
│   │   └── database/                          # Database configuration and session
│   │       ├── config.py
│   │       ├── dependencies.py
│   │       └── session.py
│   └── utils/
│       └── logger_config.py                   # Logger configuration

# Backend part
├── backend/                                   # Backend code for the application (API, server logic)
│   ├── Dockerfile                             # Dockerfile to build the backend image
│   ├── config/
│   │   └── settings.py                        # Configuration file
│   ├── logs/                                  # Log files (errors, debug, info)
│   ├── tests/                                 # Test files (pytest)
│   ├── main.py                                # FastAPI entry point
│   └── routes.py

# Frontend part
├── frontend/                                  # Frontend code of the application (Vue.js)
│   ├── Dockerfile                             # Dockerfile to build the frontend image
│   ├── index.html                             # Main HTML page
│   ├── package.json                           # Frontend dependencies and scripts (npm)
│   ├── public/                                # Public files (favicon, static assets)
│   └── src/                                   # Vue.js source code
│       ├── App.vue                            # Root Vue component
│       ├── assets/                            # Images, logos, global styles
│       │   └── logo.png
│       ├── components/                        # Reusable Vue components
│       │   ├── Auth.vue
│       │   └── Footer.vue
│       ├── functions/                         # Frontend utility functions (TS)
│       │   └── utils.ts
│       ├── main.ts                            # Vue frontend entry point
│       ├── pages/                             # Vue pages (e.g. Users.vue)
│       │   └── Users.vue
│       ├── router/                            # Vue Router route management
│       │   └── index.ts
│       ├── stores/                            # Global state storage (Pinia)
│       │   └── useAuthStore.ts
│       └── styles/                            # CSS / global styles files
│           └── styles.css

# Others
├── bonus_scripts/                             # Utility scripts for dev or management
│   ├── generate_secret_key.py                 # Script to generate a secret key (e.g. JWT)
│   └── print_tree.py                          # Script to display the project tree structure
├── docker-compose.yml                         # Docker orchestration (backend + frontend)
├── conftest.py                                # Pytest configuration file for global tests
├── requirements.txt                           # Python dependencies (local dev)
├── run_auth.py                                # Script to run authentication management (local dev)
├── run_backend.py                             # Script to run the backend (local dev)
└── run_frontend.py                            # Script to run the frontend (local dev)
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
AUTH_BACK=      # The port you want to use for the authentification part of your application
PORT_BACK=      # The port you want to use for the backend of your application
PORT_FRONT=     # The port you want to use for the frontend of your application
```

**Create and edit your initial users config file**

```sh
cp backend/modules/api/users/initial_users.yaml.example backend/modules/api/users/initial_users.yaml
```

## Launch for production

```sh
docker compose up -d --build
```

**Available services with Docker Compose**

- **Authantification / Users API** → http://localhost:{PORT_AUTH}
- **Prefect UI** → http://localhost:4200
- **Uptime Kuma** → http://localhost:3001
- **Frontend** → http://localhost:{PORT_FRONT}

**Configure Kuma**

Visit http://localhost:3001 et add the API health check : http://api:{PORT_AUTH}/health and a notification through Discord or Telegram.

## Launch in local mode

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

Open 3 different terminals:

**Backend (in terminal 1)**

```sh
python run_backend.py
```

**Frontend (in terminal 2)**

```sh
cd frontend && npm install
cd ../ && python run_frontend.py
```

**Authentification (in terminal 3)**

```sh
python run_auth.py
```

