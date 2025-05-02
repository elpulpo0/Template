# Étape 1: Build de l'application
FROM node:slim AS builder
WORKDIR /app

# Copier uniquement les fichiers de dépendances pour optimiser le cache
COPY package.json package-lock.json ./
RUN npm install

# Copier le reste des fichiers et construire l'application
COPY . .
RUN npm run build

# Étape 2: Serveur léger avec http-server
FROM node:slim

# Définir un répertoire de travail
WORKDIR /usr/share/app

# Installer http-server globalement
RUN npm install -g http-server

# Définir l'environnement en production
ENV NODE_ENV=production

# Copier les fichiers générés de la build dans le conteneur
COPY --from=builder /app/dist .

# Créer un utilisateur non-root
RUN useradd -ms /bin/bash appuser

# Changer le propriétaire des fichiers de l'application
RUN chown -R appuser:appuser /usr/share/app

# Utiliser l'utilisateur non-root pour exécuter l'application
USER appuser

# Exposer le port 8081
EXPOSE 8081

# Lancer http-server pour servir l'application
CMD ["http-server", "-p", "8081", "-s", "-c-1"]
