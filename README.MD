# POC-88 — Mempool Congestion Visualizer

**Phase 2 Deployment | Aswin Sankar P.S.**

A real-time Bitcoin mempool intelligence dashboard that analyzes transaction congestion, fee conditions, memory usage, and transaction activity using live public blockchain data.

---

## 🚀 Project Overview

**POC-88 — Mempool Congestion Visualizer** is a Phase 2 intelligence engineering application focused on Bitcoin transaction infrastructure.

The application transforms live mempool data into an interactive dashboard that helps users understand:

* Current mempool congestion
* Transaction volume
* Mempool memory utilization
* Fee conditions
* Transaction activity
* Congestion level and score
* Transaction inclusion conditions

The project demonstrates the application of the Real Rails intelligence engineering model to a blockchain infrastructure domain.

---

## 🎯 Objectives

The main objectives of POC-88 are to:

* Analyze live Bitcoin mempool activity.
* Convert raw blockchain data into actionable intelligence.
* Visualize congestion and fee-market conditions.
* Provide an interactive monitoring experience.
* Demonstrate real-time public API integration.
* Build a production-style full-stack application.
* Apply AI-assisted engineering and structured development practices.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      User / Browser  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Next.js Frontend   │
                    │   Interactive UI     │
                    └──────────┬───────────┘
                               │
                         REST API Requests
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    │   Data Processing    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Mempool.space API  │
                    │   Live Bitcoin Data  │
                    └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Responsive dashboard UI

### Backend

* Python
* FastAPI
* Uvicorn
* REST APIs

### Data Source

* Mempool.space public API

### Deployment

* **Frontend:** Vercel
* **Backend:** Render

---

## 📊 Dashboard Capabilities

The dashboard provides intelligence around:

### Mempool Activity

* Current transaction count
* Virtual memory size
* Mempool memory utilization
* Total transaction fees

### Congestion Intelligence

* Congestion score
* Congestion classification
* Current network conditions
* Transaction pressure indicators

### Fee Intelligence

* Minimum mempool fee
* Incremental relay fee
* Fee-market conditions
* Transaction inclusion estimates

### Visualization

The frontend converts backend analytics into interactive visual components so users can understand the current Bitcoin mempool state quickly.

---

## 🔌 Backend API

The FastAPI backend exposes REST endpoints for retrieving mempool and congestion information.

Example:

```text
GET /api/mempool/
```

```text
GET /api/mempool/congestion
```

The congestion endpoint returns calculated intelligence such as:

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

Values change according to the live/source data available at runtime.

---

## 🌐 Deployment

### Frontend

The Next.js frontend is deployed using **Vercel**.

### Backend

The FastAPI backend is deployed using **Render**.

The frontend communicates with the deployed backend through the configured API endpoint.

> Do not use `localhost` or `127.0.0.1` in the production frontend configuration.

---

## 🔐 Configuration

Environment variables should be configured through the deployment platforms rather than committing secrets to GitHub.

Example frontend configuration:

```env
NEXT_PUBLIC_API_URL=<DEPLOYED_BACKEND_URL>
```

Example backend configuration:

```env
PORT=8000
```

Actual production values should be configured in Vercel/Render environment settings.

---

## 💻 Local Development

### Backend

```bash
cd backend

python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

---

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

## 🐳 Docker Support

The application can be containerized using separate frontend and backend containers.

Expected architecture:

```text
Frontend Container
       │
       │ HTTP API
       ▼
Backend Container
       │
       ▼
Mempool.space API
```

The production deployment uses managed cloud platforms rather than requiring users to run the containers manually.

---

## 🔄 Data Flow

```text
Bitcoin Network
      │
      ▼
Mempool.space API
      │
      ▼
FastAPI Backend
      │
      ├── Fetch mempool data
      ├── Process metrics
      ├── Calculate congestion
      └── Prepare API response
      │
      ▼
Next.js Frontend
      │
      ▼
Interactive Intelligence Dashboard
```

---

## 🧪 Validation

The application should be validated for:

* Frontend availability
* Backend API availability
* API-to-frontend communication
* Live data retrieval
* Congestion calculations
* Dashboard rendering
* Responsive UI
* Error handling
* Production environment configuration
* Backend restart/recovery

---

## 📁 Project Structure

```text
POC-88-MempoolCongestionVisualizer-AswinSankar-Phase2/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .env.example
```

---

## 🎬 Phase 2 Focus

This Phase 2 implementation extends the initial PoC into a more complete application with emphasis on:

1. Production-oriented application structure
2. Full-stack frontend/backend integration
3. Live external data handling
4. Interactive intelligence visualization
5. Deployment readiness
6. Containerization
7. Cloud deployment
8. Validation and operational reliability

---

## 👨‍💻 Developer

**Aswin Sankar P.S.**

GitHub:

https://github.com/sankeraswin579-crypto

Repository:

https://github.com/sankeraswin579-crypto/POC-88-MempoolCongestionVisualizer-AswinSankar-Phase2

---

## 📌 Project Status

**POC-88 — Mempool Congestion Visualizer**

**Phase 2 — Deployed**

Frontend: **Vercel**

Backend: **Render**

The application is intended to demonstrate a production-oriented blockchain intelligence dashboard built using modern full-stack technologies.

---

## ⚠️ Disclaimer

This project is intended for technical demonstration, data visualization, and blockchain infrastructure analysis.

It does not provide financial advice or guarantee transaction confirmation times.
