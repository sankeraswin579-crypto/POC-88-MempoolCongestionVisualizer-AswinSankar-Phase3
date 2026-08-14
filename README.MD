# 🚀 Phase 2 — Mempool Congestion Visualizer

> **Advanced Bitcoin Mempool Analytics & Congestion Intelligence Platform**

The **Mempool Congestion Visualizer — Phase 2** is an enhanced version of the Phase 1 Proof of Concept developed to analyze and visualize real-time Bitcoin mempool activity.

Phase 2 extends the original concept by introducing a more structured application architecture, improved analytics, interactive visualizations, congestion intelligence, fee analysis, and a more polished dashboard experience.

---

## 📌 Project Information

| Field              | Details                                          |
| ------------------ | ------------------------------------------------ |
| **Project**        | Mempool Congestion Visualizer                    |
| **Phase**          | Phase 2                                          |
| **PoC ID**         | POC-88                                           |
| **Developer**      | Aswin Sankar P.S.                                |
| **GitHub**         | `sankeraswin579-crypto`                          |
| **Repository**     | `POC-88-MempoolCongestionVisualizer-AswinSankar` |
| **Data Source**    | Mempool.space API                                |
| **Status**         | Phase 2 — Local Application                      |
| **Primary Domain** | Bitcoin / Blockchain Analytics                   |

---

# 🎯 Phase 2 Objective

The primary objective of Phase 2 is to transform the initial mempool visualization concept into a more complete **Bitcoin network intelligence platform**.

### Phase 1

The original PoC focused primarily on:

```text
Bitcoin Network Data
        ↓
API Integration
        ↓
Mempool Data
        ↓
Basic Visualization
```

### Phase 2

The application expands this into:

```text
Bitcoin Network
       ↓
Mempool.space API
       ↓
Data Collection
       ↓
Data Processing
       ↓
Analytics Engine
       ↓
Congestion Analysis
       ↓
Fee Analysis
       ↓
Block Analysis
       ↓
Intelligence Layer
       ↓
Interactive Dashboard
```

The goal is to provide not only **what is happening**, but also a clearer understanding of **what the network conditions mean**.

---

# 🧩 Problem Statement

Bitcoin transactions are temporarily stored in the mempool before being included in blocks.

When transaction demand increases, competition for block space can increase, resulting in:

* Higher transaction fees
* Longer confirmation times
* Increased mempool size
* Greater transaction competition
* Difficulty selecting appropriate fees

Raw blockchain API data can be difficult for normal users to interpret.

### Phase 2 Solution

The project converts raw Bitcoin network information into an accessible analytics platform containing:

* Real-time metrics
* Congestion indicators
* Fee-market analysis
* Block statistics
* Trend visualizations
* Network intelligence
* Human-readable insights

---

# ⭐ Phase 2 Enhancements

Phase 2 focuses on improving the capabilities of the original PoC.

## 1. Enhanced Dashboard

The dashboard provides a centralized view of Bitcoin network conditions.

It presents:

* Mempool statistics
* Transaction activity
* Fee conditions
* Congestion level
* Recent block information
* Analytical insights

---

## 2. Congestion Intelligence

Instead of displaying only raw mempool values, Phase 2 introduces a congestion-analysis layer.

The system evaluates available network metrics and produces an understandable congestion condition.

Example:

```text
Network Metrics
      ↓
Feature Analysis
      ↓
Congestion Score
      ↓
Condition Classification
      ↓
User-Friendly Explanation
```

Possible conditions include:

* 🟢 Low
* 🟡 Moderate
* 🟠 High
* 🔴 Critical

---

## 3. Fee-Market Analysis

The application analyzes current Bitcoin fee conditions.

Users can understand:

* Current fee pressure
* Fee-rate conditions
* Recommended fee ranges
* Transaction priority
* Potential confirmation implications

This helps convert technical fee information into practical insights.

---

## 4. Mempool Analytics

Phase 2 provides detailed mempool information such as:

* Pending transactions
* Mempool size
* Virtual size
* Transaction pressure
* Fee distribution
* Congestion trends

---

## 5. Block Analytics

Recent Bitcoin blocks are analyzed to provide additional network context.

The dashboard can display information such as:

* Block height
* Transaction count
* Block size
* Block weight
* Fee information
* Recent block activity

---

## 6. Interactive Data Visualization

Phase 2 improves the presentation of blockchain information through interactive charts.

Visualizations can include:

* Mempool activity
* Congestion trends
* Fee distribution
* Block statistics
* Transaction activity

Charts make changes in network conditions easier to identify.

---

## 7. Network Intelligence

The Phase 2 application adds an intelligence-oriented presentation layer.

### Intelligence Signals

Identifies notable network conditions.

### Why This Matters

Explains the practical importance of the current condition.

### What To Watch

Highlights metrics or trends that users should monitor.

### Network Summary

Provides a simplified interpretation of current Bitcoin network activity.

---

# 🏗️ Phase 2 Architecture

```text
                    ┌──────────────────────┐
                    │   Bitcoin Network    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Mempool.space API  │
                    └──────────┬───────────┘
                               │
                         API Requests
                               │
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │        Python        │
                    └──────────┬───────────┘
                               │
                    Data Processing Layer
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Analytics Engine   │
                    │                      │
                    │ • Mempool Analysis   │
                    │ • Fee Analysis       │
                    │ • Block Analysis     │
                    │ • Congestion Score   │
                    └──────────┬───────────┘
                               │
                       Processed Data
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Next.js Frontend  │
                    │ React + TypeScript   │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       Interactive Dashboard    │
              │                                │
              │ Metrics │ Charts │ Insights    │
              │ Fees    │ Blocks │ Congestion  │
              └────────────────────────────────┘
```

---

# 🔄 Phase 2 Data Flow

```text
1. User opens the dashboard
             ↓
2. Frontend requests network data
             ↓
3. FastAPI receives the request
             ↓
4. Backend requests data from
   Mempool.space
             ↓
5. API returns Bitcoin network data
             ↓
6. Backend validates and processes data
             ↓
7. Analytics calculations are performed
             ↓
8. Congestion and fee conditions are derived
             ↓
9. Processed data is returned to frontend
             ↓
10. Dashboard updates metrics and charts
             ↓
11. User receives network intelligence
```

---

# 🛠️ Technology Stack

## Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS
* Recharts
* Framer Motion

## Backend

* Python
* FastAPI
* REST API

## External API

* Mempool.space API

## Development

* Visual Studio Code
* Git
* GitHub
* Node.js
* npm
* Python

---

# 📁 Phase 2 Project Structure

```text
POC-88-MempoolCongestionVisualizer-AswinSankar/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   ├── analytics/
│   └── ...
│
├── screenshots/
│   ├── dashboard.png
│   ├── congestion-analysis.png
│   ├── fee-analysis.png
│   └── block-analysis.png
│
├── README.md
├── requirements.txt
├── .gitignore
└── package.json
```

> Adjust the folder names above if your final Phase 2 implementation uses a different structure.

---

# 🔌 API Integration

The application uses the **Mempool.space API** to obtain Bitcoin network information.

The data source is used for retrieving information related to:

* Mempool statistics
* Fee estimates
* Transactions
* Blocks
* Network activity

The backend acts as an intermediary between the external API and the frontend.

```text
Frontend
   ↓
FastAPI
   ↓
Mempool.space API
   ↓
Bitcoin Network Data
   ↓
FastAPI Processing
   ↓
Frontend Dashboard
```

---

# 📊 Core Analytics

| Analytics         | Purpose                                |
| ----------------- | -------------------------------------- |
| Mempool Size      | Measures pending transaction data      |
| Transaction Count | Indicates transaction activity         |
| Fee Rate          | Measures fee-market conditions         |
| Fee Distribution  | Shows competition between transactions |
| Congestion Score  | Simplifies network congestion          |
| Congestion Level  | Classifies current network conditions  |
| Block Statistics  | Provides recent block information      |
| Trend Analysis    | Shows changes over time                |
| Network Signals   | Identifies notable conditions          |

---

# 🧠 Congestion Analysis

A conceptual congestion-analysis pipeline is:

```text
Mempool Size
Transaction Count
Fee Conditions
Block Activity
      │
      ▼
Data Normalization
      │
      ▼
Feature Analysis
      │
      ▼
Congestion Score
      │
      ▼
Congestion Classification
      │
      ▼
Network Intelligence
```

The exact scoring methodology can be adjusted according to the implementation.

---

# 💰 Fee Analysis

The fee-analysis component helps users understand the relationship between:

```text
Transaction Demand
        +
Block Space
        +
Fee Rates
        ↓
Fee Market Pressure
```

The dashboard can provide practical classifications such as:

* Low fee pressure
* Normal fee pressure
* Elevated fee pressure
* High fee pressure

---

# 📈 Visualization Layer

The Phase 2 dashboard uses interactive visualizations to represent network activity.

Potential visualizations include:

### Mempool Trend

Shows changes in mempool activity.

### Fee Trend

Shows changes in fee conditions.

### Congestion Trend

Shows whether congestion is increasing or decreasing.

### Block Analytics

Displays recent block characteristics.

### Distribution Charts

Shows the distribution of fee rates or transaction activity.

---

# 🧠 Intelligence Layer

The intelligence layer converts numerical metrics into readable insights.

Example:

```text
Current Mempool Activity
          ↓
High Transaction Pressure
          ↓
Elevated Congestion
          ↓
Higher Fee Competition
          ↓
Potentially Longer Confirmation Times
```

This makes the application useful beyond basic data visualization.

---

# 🖥️ Dashboard Components

The Phase 2 dashboard can contain:

```text
┌─────────────────────────────────────────────┐
│          MEMPOOL CONGESTION                 │
│              VISUALIZER                    │
├──────────────┬──────────────┬──────────────┤
│ Mempool Size │ Transactions │ Congestion   │
├──────────────┴──────────────┴──────────────┤
│                                             │
│           Congestion Chart                  │
│                                             │
├─────────────────────────────────────────────┤
│ Fee Market        │ Recent Blocks           │
├───────────────────┴─────────────────────────┤
│                                             │
│ Network Intelligence                        │
│                                             │
│ • Intelligence Signals                      │
│ • Why This Matters                          │
│ • What To Watch                             │
│                                             │
└─────────────────────────────────────────────┘
```

---

# ⚙️ Installation

## Prerequisites

Install:

* Python 3.11 or later
* Node.js
* npm
* Git
* Visual Studio Code

---

## Backend Setup

Open the project in VS Code.

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

Open a second terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the application:

```bash
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# 🔐 Environment Variables

If environment variables are required by the implementation, create a `.env` file.

Example:

```env
API_BASE_URL=your_api_endpoint
```

Do not commit sensitive credentials to GitHub.

Add environment files to `.gitignore` where appropriate.

---

# 🧪 Testing Checklist

Before submitting Phase 2, verify:

* [ ] Backend starts successfully
* [ ] Frontend starts successfully
* [ ] API requests work
* [ ] Mempool data loads
* [ ] Fee data loads
* [ ] Block data loads
* [ ] Congestion calculation works
* [ ] Charts render correctly
* [ ] Dashboard updates correctly
* [ ] Error handling works
* [ ] Loading states work
* [ ] Responsive design works
* [ ] No API credentials are exposed
* [ ] GitHub repository contains required files

---

# 🐛 Error Handling

The application should gracefully handle:

* API timeout
* API unavailable
* Invalid API response
* Missing data
* Network connection failure
* Backend failure
* Frontend request failure

Instead of crashing, the dashboard should provide a meaningful status or error message.

---

# 🔒 Security Considerations

The application is designed for analytics and visualization.

It does **not** require:

* Private Bitcoin keys
* Wallet credentials
* Transaction signing
* User funds
* Custodial wallet access

External API credentials, when applicable, should be stored securely using environment variables.

---

# 🎓 Skills Demonstrated

Phase 2 demonstrates practical experience in:

### Programming

* Python
* TypeScript
* JavaScript

### Backend Development

* FastAPI
* REST APIs
* API integration
* Data processing

### Frontend Development

* React
* Next.js
* Tailwind CSS
* Responsive UI

### Data & Analytics

* Data transformation
* Statistical analysis
* Trend analysis
* Data visualization
* KPI development

### Blockchain

* Bitcoin
* Mempool
* Block data
* Transaction fees
* Block space
* Network congestion

### Software Engineering

* Modular architecture
* Error handling
* Environment configuration
* Git
* GitHub
* Project documentation

---

# 🔮 Future Enhancements

Future versions could introduce:

* Historical database storage
* WebSocket-based live updates
* Machine-learning congestion prediction
* Fee forecasting
* Confirmation-time prediction
* Advanced historical analytics
* User-configurable alerts
* Cloud deployment
* Docker containerization
* Automated monitoring
* Blockchain data warehouse
* Advanced anomaly detection

---

# 📸 Screenshots

Add Phase 2 screenshots here:

```markdown
## Dashboard

![Phase 2 Dashboard](screenshots/dashboard.png)

## Congestion Analysis

![Congestion Analysis](screenshots/congestion-analysis.png)

## Fee Analysis

![Fee Analysis](screenshots/fee-analysis.png)

## Block Analytics

![Block Analytics](screenshots/block-analysis.png)
```

---

# 🏁 Phase 2 Outcome

Phase 2 transforms the original **Mempool Congestion Visualizer PoC** into a more structured and feature-rich Bitcoin network analytics application.

The project demonstrates the complete flow:

```text
Real-Time Blockchain Data
          ↓
API Integration
          ↓
Backend Processing
          ↓
Analytics
          ↓
Congestion Intelligence
          ↓
Interactive Visualization
          ↓
User-Facing Network Insights
```

The result is a practical dashboard for understanding Bitcoin mempool conditions, transaction activity, fee-market pressure, and recent block activity.

---

# 👨‍💻 Developer

**Aswin Sankar P.S**

AI & Data Science | Machine Learning | Generative AI | Data Analytics | Blockchain Analytics

**GitHub:** `sankeraswin579-crypto`

**PoC:** `POC-88`

**Project:** `Mempool Congestion Visualizer`

**Phase:** `Phase 2`

---

## 📜 Disclaimer

This project is developed as a technical Proof of Concept for educational, analytical, and internship project purposes.

It provides network information and analytics and should not be considered financial or investment advice.
