<p align="center">
  <img src="https://img.icons8.com/nolan/256/brain.png" alt="InterviewVerse AI Logo" width="120" />
</p>

<h1 align="center">🔮 InterviewVerse AI</h1>

<p align="center">
  <strong>Next-Generation AI Technical Interview Simulation Platform</strong>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&duration=3000&pause=1000&color=9C27B0&center=true&vCenter=true&width=500&lines=Gemini+AI+Powered+Interviews;Fully+Customizable+Personas;Instant+Performance+Roadmaps;Docker+Ready+%2B+GCP+Cloud+Deploy" alt="Typing SVG" />
</p>

<p align="center">
  <a href="https://github.com/logitechsoumili/interviewverse-ai/stargazers">
    <img src="https://img.shields.io/github/stars/logitechsoumili/interviewverse-ai?style=for-the-badge&color=blue&logo=github" alt="GitHub Stars" />
  </a>
  <a href="https://github.com/logitechsoumili/interviewverse-ai/network/members">
    <img src="https://img.shields.io/github/forks/logitechsoumili/interviewverse-ai?style=for-the-badge&color=purple&logo=git" alt="GitHub Forks" />
  </a>
  <a href="https://github.com/logitechsoumili/interviewverse-ai/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/logitechsoumili/interviewverse-ai?style=for-the-badge&color=green" alt="MIT License" />
  </a>
  <img src="https://komarev.com/ghpvc/?username=logitechsoumili-interviewverse-ai&color=purple&style=for-the-badge" alt="Visitor Counter" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FASTAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI Badge" />
  <img src="https://img.shields.io/badge/NEXT.JS-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js Badge" />
  <img src="https://img.shields.io/badge/TAILWIND_CSS-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind Badge" />
  <img src="https://img.shields.io/badge/POSTGRESQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL Badge" />
  <img src="https://img.shields.io/badge/DOCKER-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Badge" />
  <img src="https://img.shields.io/badge/GOOGLE_CLOUD-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" alt="GCP Badge" />
</p>

---

## 📖 About

**InterviewVerse AI** is a state-of-the-art technical interview simulation platform that prepares software engineering candidates for rigorous real-world technical assessments. Driven by Google's Gemini Large Language Model (LLM), the platform replicates the behavior of distinct tech interview personas—ranging from supportive, behavior-driven HR managers to conceptually demanding Computer Science professors and strategic tech investors. 

By analyzing the candidate's real-time transcript responses, the engine persists the session, completes full evaluation assessments, and builds a comprehensive learning roadmap to bridge core knowledge gaps.

---

## ⚡ Features

### 🎙️ AI Technical Mock Interviews
* 🤖 **Gemini AI Engine**: Simulates deep, contextual back-and-forth communication based on candidate inputs.
* 👥 **Diverse Interviewer Personas**: Choose from different built-in interviewers with unique personalities and evaluation criteria.
* 📄 **Resume Upload Integration**: Personalize conversation directions and question complexities using parsed resume highlights.

### 🛡️ Authentication & Session Management
* 🔑 **Secure Authentication**: Built on secure user accounts using **JWT (JSON Web Tokens)**.
* 🔒 **Encrypted Storage**: Secure password hashing with high-performance cryptographic defaults.
* 📂 **Interview History Retention**: Interview sessions, evaluations, and markdown reports are fully persisted in a cloud database.

### 📈 Detailed Evaluation & Feedback
* 🎯 **Fine-Grained Scoring Metrics**: Evaluates Communication, Technical Proficiency, and Confidence level out of 100.
* 🗺️ **Personalized Roadmaps**: Generates custom learning plans to strengthen areas for improvement.
* 📝 **Markdown Reports**: Complete downloadable and printable performance summary.

### 🌐 Scalable Architecture
* 📦 **Containerized Workloads**: Multi-stage root level `Dockerfile` configuring rootless processes.
* 🏗️ **Single Container Serving**: Next.js static asset exports served instantly under a FastAPI SPA router.
* ⚡ **GCP & Render Deployment Ready**: Simple, cloud-agnostic blueprints.

---

## 📐 Architecture

Below is a clean visualization of the system components and data layout:

```mermaid
graph TD
    subgraph Client ["Next.js SPA Client (Hydrated Out)"]
        UI["React components"]
        Query["React Query state"]
        Storage["LocalStorage (Session State)"]
    end

    subgraph Service ["FastAPI Application (WS / HTTP)"]
        Router["HTTP Router / Endpoints"]
        AI["AI services (Interview & evaluation)"]
        ORM["SQLAlchemy Models"]
    end

    subgraph Database ["PostgreSQL Instance (Neon / Cloud)"]
        UserTable["users"]
        SessionTable["interview_sessions"]
        PersonaTable["personas"]
        EvalTable["evaluations"]
        ReportTable["reports"]
    end

    subgraph Models ["External Upstream Models"]
        Gemini["Google Gemini LLM"]
    end

    UI <--> Query
    Query <--> |REST API| Router
    Router <--> AI
    AI <--> ORM
    ORM <--> Database
    AI <--> |gRPC / REST| Gemini
    UI <--> Storage
```

---

## 🛠️ Tech Stack

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=typescript,react,nextjs,tailwindcss,python,fastapi,postgres,docker,gcp" alt="Skill Icons" />
  </a>
</p>

* **Frontend**: Next.js (App Router, Static Export), TailwindCSS, Framer Motion, React Query, Zod.
* **Backend**: FastAPI, SQLAlchemy, Alembic, Uvicorn, Python 3.12.
* **Database**: PostgreSQL (Neon serverless or Google Cloud SQL).
* **AI/LLM**: Google GenAI SDK (Gemini Models).
* **Containerization**: Docker (Multi-stage builds, non-root configurations).
* **Deployment**: Google Cloud Platform (Cloud Run, Cloud SQL) or Render.

---

## 📂 Folder Structure

```
interviewverse-ai/
├── backend/                  # FastAPI Application Code
│   ├── alembic/              # DB Migrations and Schema Alignments
│   ├── app/                  # Main FastAPI Application
│   │   ├── api/              # API Endpoints (Auth, Interviews, Personas, Reports)
│   │   ├── core/             # Configuration and Security Defaults
│   │   ├── db/               # SQLAlchemy Session and Seeding logic
│   │   ├── models/           # SQLAlchemy Declarative Models
│   │   ├── schemas/          # Pydantic Schemas
│   │   └── services/         # Business Logic (User, AI Orchestration, Gemini)
│   ├── tests/                # Pytest Suite (146 passing tests)
│   ├── alembic.ini           # Alembic Database Migrations Config
│   └── requirements.txt      # Python Dependencies
├── frontend/                 # Next.js Application Code
│   ├── app/                  # Next.js App Router Structure
│   ├── components/           # Common Shared UI Elements (shadcn/ui)
│   ├── features/             # Feature-grouped Client Mappings (Auth, Dashboard, Interviews)
│   ├── lib/                  # State management, Http instances, Query keys
│   ├── next.config.mjs       # Static Export Configurations
│   └── tsconfig.json         # TypeScript Paths Map
├── Dockerfile                # Multi-stage production-grade single container serving
├── docker-compose.yml        # Development environment runner
├── render.yaml               # Render Blueprint Specification
└── README.md                 # Project Documentation
```

---

## 🖼️ Screenshots

<p align="center">
  <table border="1">
    <tr>
      <td width="50%" align="center">
        <strong>1. Landing Page</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Landing+Page+Mockup" alt="Landing Page" width="100%" />
      </td>
      <td width="50%" align="center">
        <strong>2. User Login</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Login+Page+Mockup" alt="Login" width="100%" />
      </td>
    </tr>
    <tr>
      <td width="50%" align="center">
        <strong>3. Dashboard Overview</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Dashboard+Overview+Mockup" alt="Dashboard" width="100%" />
      </td>
      <td width="50%" align="center">
        <strong>4. Persona Selector</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Persona+Selection+Mockup" alt="Personas" width="100%" />
      </td>
    </tr>
    <tr>
      <td width="50%" align="center">
        <strong>5. Active Chat Session</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Interview+Chat+Mockup" alt="Interview Screen" width="100%" />
      </td>
      <td width="50%" align="center">
        <strong>6. Performance Evaluation</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Evaluation+Scores+Mockup" alt="Evaluation" width="100%" />
      </td>
    </tr>
    <tr>
      <td width="50%" align="center">
        <strong>7. Comprehensive Report</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=Markdown+Report+Mockup" alt="Report" width="100%" />
      </td>
      <td width="50%" align="center">
        <strong>8. Interview History</strong><br/>
        <img src="https://placehold.co/600x400/1e1e24/a3a3c2?text=History+List+Mockup" alt="History" width="100%" />
      </td>
    </tr>
  </table>
</p>

---

## ⚙️ Environment Variables

Copy `backend/.env.example` to `backend/.env` (and similarly for frontend if customized):

| Variable Name | Description | Default / Example Value |
| :--- | :--- | :--- |
| `DATABASE_URL` | Neon/PostgreSQL Connection String | `postgresql+psycopg://user:pass@host/dbname` |
| `GEMINI_API_KEY` | Google Gemini API Access Token | `AIzaSyD-your-api-key-here` |
| `JWT_SECRET` | Secret key to sign tokens (Access + Refresh) | `your-cryptographic-secure-secret-key` |
| `JWT_ALGORITHM` | Algorithm to encrypt token payloads | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Authentication token validity duration | `60` |
| `NEXT_PUBLIC_API_URL` | Frontend endpoint mapper (defaults to proxy) | `/api/v1` |

---

## 🚀 Installation & Local Development

### 1. Prerequisite Checklist
* Install [Python 3.12+](https://www.python.org/downloads/)
* Install [Node.js v20+](https://nodejs.org/)
* Install [Docker](https://www.docker.com/) (Optional, for container setup)

### 2. Manual Environment Setup

#### Setup Backend:
```bash
cd backend
python -m venv venv
# Windows powershell:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env # Configure variables in .env
```

#### Setup Frontend:
```bash
cd ../frontend
npm install
```

### 3. Run Applications Locally

#### Running Migrations & Seeding:
```bash
# Run inside backend activation environment
alembic upgrade head
python app/db/seed.py
```

#### Launching servers:
```bash
# Start backend (Uvicorn listens on port 8000)
cd backend
uvicorn app.main:app --reload

# Start frontend (Vite dev server listens on port 3000)
cd ../frontend
npm run dev
```

### 4. Running with Docker Compose
If you prefer running fully containerized development stacks locally, launch via Compose:
```bash
docker-compose up --build
```

---

## 🚢 Google Cloud Deployment (GCP Cloud Run)

Follow this recipe to deploy the single container to Cloud Run connected to Cloud SQL:

### 1. Build and push container to Artifact Registry
```bash
# Authenticate Google Cloud CLI
gcloud auth login
gcloud config set project [PROJECT_ID]

# Create Artifact Registry Repository
gcloud artifacts repositories create interviewverse-repo \
    --repository-format=docker \
    --location=us-central1

# Build and Tag local container
docker build -t us-central1-docker.pkg.dev/[PROJECT_ID]/interviewverse-repo/app:latest .

# Configure Docker credentials helper
gcloud auth configure-docker us-central1-docker.pkg.dev

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/[PROJECT_ID]/interviewverse-repo/app:latest
```

### 2. Deploy to Cloud Run
```bash
gcloud run deploy interviewverse-service \
    --image us-central1-docker.pkg.dev/[PROJECT_ID]/interviewverse-repo/app:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="DATABASE_URL=postgresql+psycopg://[USER]:[PASS]@[CLOUD_SQL_IP]/[DB_NAME],GEMINI_API_KEY=[API_KEY],JWT_SECRET=[SECRET]"
```

---

## 🧬 API Endpoints

<details>
<summary>🔑 Authentication Endpoints</summary>

| Verb | Path | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | No | Registers a new user. Returns user metadata. |
| `POST` | `/api/v1/auth/login` | No | Authenticates user credentials. Returns JWT. |
</details>

<details>
<summary>👥 Persona Endpoints</summary>

| Verb | Path | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/personas` | Yes | Retrieves list of available built-in interview personas. |
| `POST` | `/api/v1/personas` | Yes | Creates a custom user interviewer persona. |
</details>

<details>
<summary>🎙️ Interview Endpoints</summary>

| Verb | Path | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interviews/start` | Yes | Initiates session, records details, yields opening turn. |
| `POST` | `/api/v1/interviews/{id}/message` | Yes | Appends candidate message, fetches dynamic follow-up. |
| `POST` | `/api/v1/interviews/{id}/complete` | Yes | Flags session as completed and closes transactions. |
| `GET` | `/api/v1/interviews` | Yes | Lists all past and active interviews for logged user. |
| `GET` | `/api/v1/interviews/{id}` | Yes | Fetches metadata and message turns for the session ID. |
</details>

<details>
<summary>📊 Evaluations & Reports Endpoints</summary>

| Verb | Path | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interviews/{id}/evaluate` | Yes | Computes scores and roadmap. Persists to DB. |
| `GET` | `/api/v1/interviews/{id}/evaluation` | Yes | Fetches persisted evaluation metrics. |
| `GET` | `/api/v1/interviews/{id}/report` | Yes | Generates and compiles printable performance report. |
</details>

---

## 🌀 User Workflow Flowchart

Below is the state transitions of a user going through the mock interview process:

```mermaid
flowchart TD
    Start([1. User landing page]) --> Register[2. Registration / Account Setup]
    Register --> Login[3. JWT Authentication Login]
    Login --> Persona[4. Choose Interview Persona]
    Persona --> StartInterview[5. POST /interviews/start]
    StartInterview --> Conversation{6. Conversation Loop}
    Conversation --> |Candidate Types Answer| SendMessage[7. POST /message]
    SendMessage --> |AI Generates follow-up| Conversation
    Conversation --> |Time limit or candidate clicks End| Complete[8. POST /complete]
    Complete --> Evaluate[9. POST /evaluate]
    Evaluate --> Report[10. GET /report]
    Report --> History[11. Stored in history page]
```

---

## 🔮 Future Improvements

* [ ] 🎙️ **Speech-to-Text & Text-to-Speech**: Implement real-time voice conversations using WebRTC or WebSocket audio streaming.
* [ ] 📈 **Comparative Analytics**: Visual dashboards tracing progress score improvements over time.
* [ ] 📂 **GitHub / LinkedIn Auto-Import**: Auto-generate custom personas based on target job listings.
* [ ] 👨‍👩‍👦 **Multiplayer Mocking**: Mock interview mode with peer-review panels and custom scorecards.

---

## 👥 Contributors

<p align="center">
  <a href="https://github.com/logitechsoumili/interviewverse-ai/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=logitechsoumili/interviewverse-ai" alt="Contributors List" />
  </a>
</p>

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 💖 Acknowledgements

* [Google Gemini AI API](https://ai.google.dev/)
* [FastAPI Framework](https://fastapi.tiangolo.com/)
* [Next.js App Router](https://nextjs.org/)
* [Tailwind CSS](https://tailwindcss.com/)
* [Neon Serverless PostgreSQL](https://neon.tech/)
* [Shields.io Badges](https://shields.io/)
* [Docker Containers](https://www.docker.com/)