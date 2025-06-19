FROM node:alpine AS builder
WORKDIR /app

ARG VITE_APP_NAME
ARG VITE_GITHUB_URL

ENV VITE_APP_NAME=$VITE_APP_NAME
ENV VITE_GITHUB_URL=$VITE_GITHUB_URL

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build
RUN cp build-meta.json dist/

FROM node:alpine

WORKDIR /usr/share/app

RUN npm install -g http-server

ENV NODE_ENV=production

COPY --from=builder /app/dist .

RUN apk add --no-cache shadow bash

RUN useradd -ms /bin/bash appuser

RUN chown -R appuser:appuser /usr/share/app

USER appuser

EXPOSE 8081

CMD ["http-server", "-p", "8081", "-s", "-c-1"]
