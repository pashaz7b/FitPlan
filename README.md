# 🏋️‍♂️ FitPlan

**FitPlan** is a modular gym management platform built with a microservice architecture. It enables seamless interaction between users and their coaches, offering features such as workout planning, real-time chat, and secure authentication.

This project is developed using **FastAPI**, **PostgreSQL**, **Redis**, and **Docker**, and is structured for scalability, maintainability, and modern deployment workflows.

---

## 🌟 Features

- ⚙️ Microservice-based architecture
- 🔐 JWT-based authentication via IAM service
- 💬 Real-time chat between users and coaches using WebSocket
- 🗓️ Workout program management
- 🧠 Decoupled services for flexibility and scaling
- 📃 Auto-generated API documentation via Swagger UI

---

## 🧱 Project Structure

```bash
FitPlan/
├── backend/
│   ├── services/
│   │   ├── iam-service/         # Identity and Authentication
│   │   ├── media-service/        # Chat service using WebSocket
│   │   ├── core-service/     # Workout planning service
│   │   └── chat-service/       # chat services
│   └── deployment/              # Docker and Kubernetes files
├── frontend/                    # Frontend app (optional or WIP)
└── README.md
