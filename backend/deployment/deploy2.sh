#!/bin/bash

# Use multiple -f flags to include all service-specific and infrastructure Compose files
docker compose -f docker-compose.yml \
               -f ../infra/api-gateway/docker-compose.yml \
               -f ../services/chat-service/docker-compose.yml \
               up -d --build


