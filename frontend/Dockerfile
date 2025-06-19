# Étape 1: Build de l'application
FROM node:alpine AS builder
WORKDIR /app

# ARG
ARG VITE_APP_NAME
ARG VITE_GITHUB_URL

ENV VITE_APP_NAME=$VITE_APP_NAME
ENV VITE_GITHUB_URL=$VITE_GITHUB_URL

# Copier uniquement les fichiers de dépendances pour optimiser le cache
COPY package.json package-lock.json ./
RUN npm install

# Copier le reste des fichiers et construire l'application
COPY . .
RUN npm run build
RUN cp build-meta.json dist/

# Étape 2: Serveur léger avec http-server
FROM node:alpine

# Définir un répertoire de travail
WORKDIR /usr/share/app

# Installer http-server globalement
RUN npm install -g http-server

# Définir l'environnement en production
ENV NODE_ENV=production

# Copier les fichiers générés de la build dans le conteneur
COPY --from=builder /app/dist .

# Installer 'shadow' pour avoir useradd, et bash
RUN apk add --no-cache shadow bash

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
