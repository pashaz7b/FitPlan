#!/bin/bash

echo "📦 Deploying Backend..."
(cd backend/deployment && ./deploy.sh)

echo "🎨 Deploying Frontend..."
(cd frontend/fit-plan && ./deploy.sh)

echo "✅ All services are up and running!"
