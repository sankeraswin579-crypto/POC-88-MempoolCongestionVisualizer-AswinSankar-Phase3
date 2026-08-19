# 🐳 POC-88 — Mempool Congestion Visualizer

**Infocreon Internship — Phase 2: Local-to-Cloud Containerization**

A containerized Bitcoin network intelligence dashboard that visualizes real-time mempool congestion, transaction activity, fee-market conditions, and recent blockchain activity.

The application uses a **Next.js frontend** and **FastAPI backend**, orchestrated with **Docker Compose** for a reproducible local environment suitable for future cloud deployment.

---

## 📌 Project Overview

The **Mempool Congestion Visualizer** provides an intelligence-focused view of the Bitcoin network by transforming live mempool and blockchain data into understandable network-pressure indicators.

### Key capabilities

* Real-time mempool monitoring
* Congestion score calculation
* Network pressure classification
* Pending transaction monitoring
* Mempool virtual-size analysis
* Memory utilization monitoring
* Fee-market analysis
* Fast and economy fee recommendations
* Fee-rate distribution visualization
* Recent Bitcoin block information
* Network intelligence insights
* Live frontend/backend communication
* Dockerized deployment architecture

---

## 🏗️ Architecture

```text
                    ┌─────────────────────────┐
                    │     Mempool.space API   │
                    │   Bitcoin Network Data  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend      │
                    │        Port 8000         │
                    │                         │
                    │ /api/mempool/            │
                    │ /api/mempool/congestion │
                    │ /api/analytics/dashboard│
                    │ /api/analytics/          │
                    │ intelligence             │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Next.js Frontend     │
                    │        Port 3000         │
                    │                         │
                    │ Mempool Dashboard       │
                    │ Charts & Analytics      │
                    │ Network Intelligence    │
                    └─────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend

* Next.js
* React
* JavaScript / TypeScript
* Responsive dashboard UI
* Data visualization

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* REST API architecture
* Requests / HTTP-based data integration

### Infrastructure

* Docker
* Docker Compose
* Linux-based containers
* WSL2 on Windows
* Container health checks

### Data Source

* Mempool.space
* Bitcoin mempool and blockchain data

---

## 📁 Project Structure

```text
POC-88-MempoolCongestionVisualizer-AswinSankar-Phase2/
│
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json
│   ├── next.config.*
│   └── application source
│
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   ├── main.py
│   └── application source
│
├── docs/
│   ├── DOCKER_SETUP.md
│   ├── ENVIRONMENT_CONFIGURATION.md
│   ├── LOCAL_CONTAINER_VALIDATION.md
│   └── TROUBLESHOOTING.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
└── repomix-output.xml
```

> The exact repository structure may vary according to the current implementation.

---

# 🚀 Getting Started

## Prerequisites

Install the following before running the project:

* Git
* Docker Desktop
* Docker Compose
* WSL2 on Windows
* Internet connectivity for live Mempool.space data

Verify Docker:

```powershell
docker --version
```

Verify Docker Compose:

```powershell
docker compose version
```

Verify WSL:

```powershell
wsl --status
```

---

# 🔐 Environment Configuration

Create a local `.env` file if required by the current implementation.

Use `.env.example` as the safe configuration template.

Example:

```env
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### Security

Never commit:

* API keys
* Passwords
* Access tokens
* Azure credentials
* Database credentials
* Private certificates
* Secret connection strings

The actual `.env` file should remain excluded through `.gitignore`.

---

# 🐳 Docker Setup

## Build the application

From the project root:

```powershell
docker compose build
```

## Start the containers

```powershell
docker compose up
```

Or run in detached mode:

```powershell
docker compose up -d
```

## Check container status

```powershell
docker compose ps
```

Expected services:

```text
poc88-backend
poc88-frontend
```

The backend should report:

```text
Up (healthy)
```

---

# 🌐 Application URLs

### Frontend

```text
http://localhost:3000
```

### Backend

```text
http://localhost:8000
```

### FastAPI Documentation

```text
http://localhost:8000/docs
```

### Backend Health Check

```text
http://localhost:8000/health
```

---

# 🔌 API Endpoints

## Health

```http
GET /health
```

Used to verify backend availability.

---

## Mempool Data

```http
GET /api/mempool/
```

Provides current mempool information.

---

## Congestion Intelligence

```http
GET /api/mempool/congestion
```

Example response:

```json
{
  "score": 21.69,
  "level": "Low",
  "transaction_count": 84451,
  "virtual_size": 44564682,
  "memory_usage_percent": 14.85,
  "total_fee": 17084034,
  "mempool_min_fee": 0,
  "incremental_relay_fee": 0
}
```

---

## Analytics Dashboard

```http
GET /api/analytics/dashboard
```

Provides dashboard-level mempool analytics including:

* Mempool statistics
* Fee histogram
* Transaction information
* Network metrics
* Blockchain activity

---

## Network Intelligence

```http
GET /api/analytics/intelligence
```

Provides higher-level interpretation of current network conditions.

---

# 📊 Dashboard Features

The dashboard presents:

### Network State

Displays the current Bitcoin network pressure classification.

### Congestion Score

A normalized score from:

```text
0 → 100
```

used to represent current mempool pressure.

### Mempool Pressure

Visualizes recent network congestion observations.

### Fee Market

Displays fee-rate information and transaction competition for block space.

### Fee Recommendations

Provides fast-confirmation and economy fee references.

### Pending Transactions

Shows transactions currently waiting in the mempool.

### Mempool Size

Displays virtual transaction size currently occupying the mempool.

### Memory Usage

Shows the percentage of node memory associated with the mempool.

### Fee Distribution

Visualizes transaction volume across fee-rate ranges.

### Recent Bitcoin Blocks

Displays recent block activity when available.

### Network Intelligence

Provides contextual interpretation of current network conditions.

---

# 🧪 Local Container Validation

The application has been validated using Docker Compose.

## Container status

```powershell
docker compose ps
```

Validated services:

```text
poc88-backend
poc88-frontend
```

Backend:

```text
Healthy
```

Frontend:

```text
Running
```

---

## Backend API Validation

The following endpoint was successfully verified:

```powershell
Invoke-WebRequest `
  -Uri "http://localhost:8000/api/mempool/congestion" `
  -UseBasicParsing
```

Result:

```text
StatusCode : 200
```

The analytics endpoint was also verified:

```powershell
Invoke-WebRequest `
  -Uri "http://localhost:8000/api/analytics/dashboard" `
  -UseBasicParsing
```

Result:

```text
StatusCode : 200
```

---

# 🔗 Frontend-to-Backend Validation

The containerized frontend successfully communicates with the FastAPI backend.

Validated API requests include:

```text
GET /api/mempool/congestion       200 OK
GET /api/analytics/dashboard      200 OK
GET /api/analytics/intelligence   200 OK
GET /health                       200 OK
```

This confirms the frontend/backend handshake is functioning inside the Docker environment.

---

# 🔄 Restart Validation

The application was tested through a container restart cycle.

Stop:

```powershell
docker compose down
```

Start:

```powershell
docker compose up -d
```

Verify:

```powershell
docker compose ps
```

Expected:

```text
poc88-backend    Up ... (healthy)
poc88-frontend   Up ...
```

After restart, the backend continued returning successful API responses and the frontend remained accessible.

---

# 📋 Logs

## Backend logs

```powershell
docker compose logs backend
```

Recent successful requests include:

```text
GET /health 200 OK
GET /api/mempool/congestion 200 OK
GET /api/analytics/dashboard 200 OK
GET /api/analytics/intelligence 200 OK
```

## Frontend logs

```powershell
docker compose logs frontend
```

Expected startup information:

```text
Next.js
Local: http://localhost:3000
Network: http://0.0.0.0:3000
Ready
```

---

# 🛑 Stop the Application

```powershell
docker compose down
```

---

# 🔁 Restart the Application

```powershell
docker compose restart
```

Or perform a complete restart:

```powershell
docker compose down
docker compose up -d
```

---

# 🧹 Rebuild Containers

If Dockerfiles or dependencies change:

```powershell
docker compose down
docker compose build
docker compose up -d
```

---

# 🐛 Troubleshooting

## Docker command not recognized

Verify Docker Desktop is installed and running:

```powershell
docker --version
```

Then verify:

```powershell
docker compose version
```

---

## Backend is unhealthy

Check:

```powershell
docker compose logs backend
```

Then verify:

```text
http://localhost:8000/health
```

---

## Frontend is not loading

Check:

```powershell
docker compose logs frontend
```

Then open:

```text
http://localhost:3000
```

---

## Dashboard displays zero data

Verify the backend:

```powershell
Invoke-WebRequest `
  -Uri "http://localhost:8000/api/mempool/congestion" `
  -UseBasicParsing
```

Then check:

```powershell
docker compose logs backend --tail=100
```

The application requires access to its configured external Bitcoin data source for live network information.

---

## Backend API returns 502

A `502 Bad Gateway` from the analytics endpoints can indicate that the backend cannot reach the upstream Mempool.space data source.

Check external connectivity and then retry:

```powershell
docker compose restart backend
```

---

# 📦 Repomix

Generate an up-to-date project context from the Phase 2 repository root:

```powershell
npx repomix
```

This generates the project context used for architecture review and cloud-readiness workflows.

---

# 🔐 Git Safety

Before pushing changes:

```powershell
git status
```

Ensure `.env` and other secret-containing files are not staged.

Then:

```powershell
git add .
git commit -m "Complete Phase 2 Docker validation"
git push
```

---

# 📸 Validation Evidence

Recommended Phase 2 evidence:

1. Successful Docker image build
2. Running frontend and backend containers
3. `docker compose ps`
4. Frontend dashboard running
5. Working visualization
6. Backend API returning `200 OK`
7. Backend logs
8. Frontend logs
9. Successful container restart
10. Frontend/backend communication after restart

---

# 🎯 Phase 2 Status

| Validation                        | Status |
| --------------------------------- | ------ |
| Docker installation               | ✅ PASS |
| WSL2 environment                  | ✅ PASS |
| Backend container                 | ✅ PASS |
| Frontend container                | ✅ PASS |
| Backend health check              | ✅ PASS |
| Mempool API                       | ✅ PASS |
| Analytics API                     | ✅ PASS |
| Frontend-to-backend communication | ✅ PASS |
| Live data loading                 | ✅ PASS |
| Container restart validation      | ✅ PASS |
| Docker Compose                    | ✅ PASS |
| Dashboard visualization           | ✅ PASS |
| Phase 2 Docker validation         | ✅ PASS |

---

# 👨‍💻 Developer

**Aswin Sankar P.S**

**Role:** AI Engineer Intern — Infocreon

**PoC:** POC-88

**Project:** Mempool Congestion Visualizer

**Phase:** Phase 2 — Local-to-Cloud Containerization

---

# 📌 Current Status

**Ready for Docker Review**

The application successfully runs as a containerized frontend/backend system with live Bitcoin mempool data, verified API communication, successful restart behaviour, and Docker Compose orchestration.
