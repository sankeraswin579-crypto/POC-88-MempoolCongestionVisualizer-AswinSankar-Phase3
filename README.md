# POC-88 Ã¢â‚¬â€ Mempool Congestion Visualizer

## Phase 3 Ã¢â‚¬â€ Data Foundation, Dockerization & Production Readiness

**Project:** Mempool Congestion Visualizer
**Developer:** Aswin Sankar P.S.
**Phase:** Phase 3
**Repository:** `POC-88-MempoolCongestionVisualizer-AswinSankar-Phase3`

---

## 1. Project Overview

POC-88 Mempool Congestion Visualizer is a full-stack data visualization and intelligence application designed to monitor and explain Bitcoin mempool activity.

The application retrieves live blockchain mempool information, processes congestion-related metrics through a FastAPI backend, and presents the results through an interactive Next.js dashboard.

### Phase 3 Focus

Phase 3 extends the Phase 2 implementation by establishing a cleaner and more deployment-ready project foundation.

The main objectives are:

* Establish a structured data foundation
* Improve backend and frontend integration
* Prepare the application for containerized execution
* Introduce Docker/Docker Compose configuration
* Improve environment-variable management
* Organize documentation and project evidence
* Maintain a clean GitHub repository
* Prepare the application for reliable deployment and testing

---

# 2. Key Features

### Live Mempool Data

The application consumes blockchain mempool information through the `mempool.space` API.

Example data includes:

* Transaction count
* Virtual size
* Mempool memory usage
* Fee information
* Congestion indicators
* Transaction activity

---

### Congestion Analysis

The backend processes the retrieved data and calculates a congestion score.

The dashboard can classify congestion into states such as:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

This provides a simplified interpretation of raw blockchain network activity.

---

### Interactive Dashboard

The frontend provides visual representations of the processed data.

Dashboard components include:

* Congestion score
* Transaction metrics
* Memory usage
* Virtual size
* Fee metrics
* Historical/visual analytics
* Status indicators
* Responsive UI components

---

# 3. System Architecture

```text
                    Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
                    Ã¢â€â€š   Mempool.space API  Ã¢â€â€š
                    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
                               Ã¢â€â€š
                               Ã¢â€“Â¼
                    Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
                    Ã¢â€â€š     FastAPI Backend  Ã¢â€â€š
                    Ã¢â€â€š                      Ã¢â€â€š
                    Ã¢â€â€š Data Retrieval       Ã¢â€â€š
                    Ã¢â€â€š Processing           Ã¢â€â€š
                    Ã¢â€â€š Congestion Analysis  Ã¢â€â€š
                    Ã¢â€â€š REST API             Ã¢â€â€š
                    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
                               Ã¢â€â€š
                         REST / JSON
                               Ã¢â€â€š
                               Ã¢â€“Â¼
                    Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
                    Ã¢â€â€š   Next.js Frontend   Ã¢â€â€š
                    Ã¢â€â€š                      Ã¢â€â€š
                    Ã¢â€â€š Dashboard            Ã¢â€â€š
                    Ã¢â€â€š Charts               Ã¢â€â€š
                    Ã¢â€â€š Metrics              Ã¢â€â€š
                    Ã¢â€â€š Visual Analytics     Ã¢â€â€š
                    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

---

# 4. Technology Stack

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
* REST APIs
* HTTP/API integration
* Data processing

## Data Source

* Mempool.space API

## DevOps

* Docker
* Docker Compose
* Environment variables
* Containerized development

## Development Tools

* Git
* GitHub
* Visual Studio Code
* PowerShell

---

# 5. Backend

The backend is implemented using FastAPI.

Its responsibilities include:

1. Connecting to the external mempool API
2. Retrieving current mempool information
3. Processing the raw API response
4. Calculating congestion-related metrics
5. Returning structured JSON responses
6. Providing REST endpoints for the frontend

Example endpoint:

```text
GET /api/mempool/congestion
```

Example response structure:

```json
{
  "score": 20.83,
  "status": "Low",
  "transactions": 86902,
  "vsize": 39874437,
  "memory_usage": 13.29
}
```

---

# 6. Frontend

The frontend is built with Next.js and React.

It consumes backend REST endpoints and converts the returned data into an interactive dashboard.

The frontend is responsible for:

* API communication
* Dashboard rendering
* Data visualization
* Responsive layout
* Metric cards
* Charts
* Status indicators
* User-friendly interpretation of blockchain data

---

# 7. Data Foundation

Phase 3 establishes a structured foundation for handling mempool data.

### Data Flow

```text
External API
     Ã¢â€ â€œ
API Response
     Ã¢â€ â€œ
FastAPI
     Ã¢â€ â€œ
Data Validation
     Ã¢â€ â€œ
Metric Processing
     Ã¢â€ â€œ
Congestion Calculation
     Ã¢â€ â€œ
JSON Response
     Ã¢â€ â€œ
Next.js
     Ã¢â€ â€œ
Charts + Dashboard
```

The architecture separates data acquisition, processing, API delivery, and visualization.

This makes the application easier to test, maintain and extend.

---

# 8. Congestion Score

The application converts multiple mempool indicators into a simplified congestion score.

Relevant indicators include:

* Number of transactions
* Mempool virtual size
* Memory utilization
* Fee pressure
* Network activity

The resulting score is presented as an interpretable congestion status.

Example:

```text
Score: 20.83

Status:
LOW
```

The scoring mechanism is intended as a dashboard interpretation layer rather than a replacement for detailed blockchain network analysis.

---

# 9. Dockerization

Phase 3 introduces containerization preparation for the application.

The project includes:

```text
docker-compose.yml
```

The intended container architecture separates the application into independently manageable services.

```text
Docker Compose
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Backend
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ FastAPI
Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Frontend
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Next.js
```

Benefits include:

* Reproducible development environment
* Simplified setup
* Service isolation
* Consistent runtime configuration
* Easier deployment
* Easier testing

---

# 10. Environment Configuration

Sensitive configuration should not be hard-coded into the source code.

The project includes:

```text
.env.example
```

Developers can create their local environment configuration from this template.

Example:

```text
BACKEND_URL=
NEXT_PUBLIC_API_URL=
```

Actual secrets and private configuration should remain outside GitHub.

---

# 11. Project Structure

```text
POC-88-MempoolCongestionVisualizer-AswinSankar-Phase3/
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ backend/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ API implementation
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ data processing
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ congestion logic
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ frontend/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Next.js application
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ dashboard components
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ charts
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ UI components
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ docs/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ project documentation
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ phase documentation
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ screenshots/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ project evidence
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ docker-compose.yml
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ .env.example
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ package-lock.json
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ README.md
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ README.MD
```

---

# 12. Local Development

## Clone Repository

```bash
git clone <repository-url>
cd POC-88-MempoolCongestionVisualizer-AswinSankar-Phase3
```

---

## Backend

Navigate to the backend:

```powershell
cd backend
```

Create/activate the Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run FastAPI:

```powershell
uvicorn main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

# 13. Frontend

Open another terminal.

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start development server:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# 14. Docker Execution

From the project root:

```powershell
docker compose up --build
```

To run in detached mode:

```powershell
docker compose up --build -d
```

To stop the containers:

```powershell
docker compose down
```

To view running containers:

```powershell
docker compose ps
```

To view logs:

```powershell
docker compose logs
```

---

# 15. API Testing

FastAPI provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

Test:

```text
GET /api/mempool/congestion
```

The endpoint should return structured mempool and congestion information.

---

# 16. Testing Checklist

### Backend

* [ ] FastAPI starts successfully
* [ ] API endpoint responds
* [ ] External API connection works
* [ ] Data is processed correctly
* [ ] Congestion score is returned
* [ ] Error handling works

### Frontend

* [ ] Next.js starts successfully
* [ ] Dashboard loads
* [ ] Backend API connection works
* [ ] Metrics render correctly
* [ ] Charts render correctly
* [ ] Responsive layout works

### Docker

* [ ] Docker image builds successfully
* [ ] Backend container starts
* [ ] Frontend container starts
* [ ] Services communicate correctly
* [ ] Environment configuration works

---

# 17. Phase 3 Engineering Objectives

Phase 3 demonstrates practical experience in:

### Software Engineering

* Full-stack application development
* REST API development
* Frontend/backend integration
* Modular project structure
* Environment configuration
* Error handling

### Data Engineering

* External API ingestion
* Data transformation
* Metric calculation
* Structured JSON data
* Data visualization pipeline

### AI/Data/Analytics Engineering

* Real-time data interpretation
* Analytical scoring
* Dashboard intelligence
* Visualization of operational metrics
* Data-driven status classification

### DevOps

* Docker
* Docker Compose
* Containerized services
* Environment management
* Deployment preparation

### Version Control

* Git
* GitHub
* Branch management
* Repository migration
* Merge conflict resolution
* Clean working tree management

---

# 18. Phase 3 Repository History

The Phase 3 repository was initialized and migrated into the dedicated GitHub repository.

Important repository operations included:

```text
Repository initialization
        Ã¢â€ â€œ
Remote configuration
        Ã¢â€ â€œ
Fetch existing repository state
        Ã¢â€ â€œ
Merge repository initialization
        Ã¢â€ â€œ
Resolve repository history
        Ã¢â€ â€œ
Push Phase 3 implementation
        Ã¢â€ â€œ
Verify origin/main
        Ã¢â€ â€œ
Clean working tree
```

Final repository state:

```text
Branch: main
Remote: origin/main
Status: Up to date
Working tree: Clean
```

---

# 19. Phase 2 Ã¢â€ â€™ Phase 3 Evolution

```text
PHASE 2
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ POC implementation
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ FastAPI backend
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Next.js frontend
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Mempool.space integration
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Dashboard
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Cloud deployment/testing
        Ã¢â€â€š
        Ã¢â€“Â¼
PHASE 3
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Data foundation
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Structured architecture
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Dockerization
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Environment configuration
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Documentation
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Evidence organization
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ Repository migration
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ Production-readiness preparation
```

---

# 20. Practical Engineering Outcome

This project demonstrates the ability to build a complete data-driven web application from external data ingestion through backend processing and frontend visualization.

The implementation combines:

```text
Python
+
FastAPI
+
REST APIs
+
External Data
+
Data Processing
+
Next.js
+
React
+
TypeScript
+
Data Visualization
+
Docker
+
Git/GitHub
```

into a single full-stack engineering workflow.

---

# 21. Skills Demonstrated

```text
Python
FastAPI
REST API Development
Next.js
React
TypeScript
Tailwind CSS
Recharts
Framer Motion
API Integration
Data Processing
Data Visualization
Real-Time Data
Docker
Docker Compose
Environment Configuration
Git
GitHub
Full-Stack Development
Backend Development
Frontend Development
Data Engineering
Analytics Engineering
Cloud Deployment Preparation
```

---

# 22. Developer

**Aswin Sankar P.S.**

AI Engineer | AI/ML | Data Science | Generative AI | Full-Stack Development

Practical focus:

* AI Engineering
* Machine Learning
* Data Science
* Generative AI
* RAG
* Agentic AI
* Python
* Full-Stack Development
* Backend APIs
* Data Engineering
* Cloud & Deployment
* Data Visualization

---

## Project Signature

```text
Designed & Transformed By
Aswin Sankar P.S.

Real Rails Internship
POC-88 Ã¢â‚¬â€ Mempool Congestion Visualizer
Phase 3
```

---

## License

This project is developed for educational, internship, portfolio, demonstration and engineering evaluation purposes.
