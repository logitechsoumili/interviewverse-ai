<p align="center">
  <a href="https://github.com/logitechsoumili/interviewverse-ai">
    <img src="https://raw.githubusercontent.com/logitechsoumili/interviewverse-ai/main/assets/banner.png" width="100%" alt="InterviewVerse AI Banner">
  </a>
</p>

<p align="center">
  <img src="https://img.icons8.com/nolan/256/brain.png" alt="InterviewVerse AI Logo" width="100" />
</p>

<h1 align="center">🔮 InterviewVerse AI</h1>

<p align="center">
  <strong>An Intelligent, Multi-Persona Technical Interview Simulation Engine powered by Gemini AI.</strong>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&duration=3500&pause=1000&color=A855F7&center=true&vCenter=true&width=600&lines=Evaluate+Candidate+Core+Strengths;Seeded+Multi-Persona+Simulation+Interviews;Detailed+Performance+Learning+Roadmaps;Production-Ready+Docker+%2B+GCP+Blueprints" alt="Typing SVG" />
</p>

---

## 📌 Table of Contents

- [📖 About](#-about)
- [⚡ Features](#-features)
- [📐 Architecture](#-architecture)
- [🛠️ Tech Stack](#-tech-stack)
- [📂 Folder Structure](#-folder-structure)
- [🖼️ Screenshots](#-screenshots)
- [🚀 Installation](#-installation)
- [🧬 API Endpoints](#-api-endpoints)
- [⚙️ Environment Variables](#-environment-variables)
- [🌀 Workflow](#-workflow)
- [🔮 Future Improvements](#-future-improvements)
- [👥 Contributors](#-contributors)
- [📄 License](#-license)

---

## 📖 About

**InterviewVerse AI** is a professional, production-grade technical interview simulation platform designed to prepare engineers for high-stakes technical assessments. The platform uses Google's Gemini Large Language Model (LLM) to power realistic mock interviews led by distinct, custom-designed personas. 

Every session is persisted in a database, allowing users to pause, resume, and review their history. Upon completing a session, the simulation engine generates granular scores (Communication, Technical, Confidence), highlights specific strengths/weaknesses, and maps out a personalized learning roadmap.

---

## ⚡ Features

- [x] 🎙️ **AI Mock Interviews**: Adaptive, real-time conversation flows driven by state-of-the-art Gemini LLM.
- [x] 👥 **Multiple Interview Personas**: Experience diverse interview styles (e.g., HR representative, CS Professor, Tech Investor).
- [x] 📄 **Resume-Based Interviews**: Custom interview adjustments driven by parsed candidate resume highlights.
- [x] 💬 **Real-time Conversation**: Seamless message streaming and instant AI follow-ups.
- [x] 🧠 **Gemini AI**: Deep context retention and multi-turn prompt engineering.
- [x] 🔑 **JWT Authentication**: Secure user registration, sign-in, and state mapping.
- [x] 🔒 **Secure Login**: Session tokens verified under industry-standard cryptographic algorithms.
- [x] 💾 **PostgreSQL Database**: Persistent data storage for user accounts, persona metadata, and histories.
- [x] 📂 **Interview History**: Chronological storage of user interview lists, complete with resume features.
- [x] 📊 **AI Evaluation**: Automatic scoring of technical and behavioral answers.
- [x] 📝 **Detailed Reports**: Highly readable, downloadable performance summaries.
- [x] 📈 **Dashboard Analytics**: High-level telemetry of overall scores and completed milestones.
- [x] 📱 **Responsive UI**: Fully optimized layout for desktop, tablet, and mobile browsers.
- [x] 🐳 **Docker Deployment**: Clean, multi-stage production container setups.

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

### 💻 Frontend
<p align="left">
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white" />
</p>

### ⚙️ Backend
<p align="left">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F26?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/Alembic-000000?style=for-the-badge&logo=alembic&logoColor=white" />
</p>

### 💾 Database & AI
<p align="left">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" />
</p>

### 🐳 Deployment & Containerization
<p align="left">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" />
</p>

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
<table>
<tr>
<td width="50%" align="center">

<strong>1. Landing Page</strong><br>

<img src="https://github.com/user-attachments/assets/ae0b89a9-11cd-4cb6-9227-4da96cdbc366" alt="Landing Page" width="100%">

</td>

<td width="50%" align="center">

<strong>2. User Login</strong><br>

<img src="https://github.com/user-attachments/assets/3788b756-343c-4f6a-bfb0-9812d7bbda28" alt="Login" width="100%">

</td>
</tr>

<tr>
<td width="50%" align="center">

<strong>3. Dashboard Overview</strong><br>

<img src="https://github.com/user-attachments/assets/b63d743e-fd73-46d0-83eb-bad82a4233a0" alt="Dashboard" width="100%">

</td>

<td width="50%" align="center">

<strong>4. Persona Selector</strong><br>

<img src="https://github.com/user-attachments/assets/c703225c-9fb4-407e-8e7d-d2d3d2c60e41" alt="Persona Selector" width="100%">

</td>
</tr>

<tr>
<td width="50%" align="center">

<strong>5. Active Chat Session</strong><br>

<img src="https://github.com/user-attachments/assets/d99d8ee4-6926-4ba8-8abb-13b9c6510efa" alt="Interview Screen" width="100%">

</td>

<td width="50%" align="center">

<strong>6. Performance Evaluation</strong><br>

<img src="https://github.com/user-attachments/assets/4c4865d9-1104-4072-897e-1d682194e1b0" alt="Evaluation" width="100%">

</td>
</tr>

<tr>
<td width="50%" align="center">

<strong>7. Comprehensive Report</strong><br>

<img src="https://github.com/user-attachments/assets/3f8f19a1-e29f-4946-8e5b-b96703505824" alt="Report" width="100%">

</td>

<td width="50%" align="center">

<strong>8. Interview History</strong><br>

<img src="https://github.com/user-attachments/assets/71a06713-ff61-4fd1-9706-4555dd5a4fbb" alt="History" width="100%">

</td>
</tr>
</table>
</p>

---

## 🚀 Installation & Local Development

### 1. Prerequisites
* Install Python 3.12+
* Install Node.js v20+
* Install Docker Desktop (Optional)

### 2. Backend Setup
Activate a virtual environment and load required dependencies:
```bash
cd backend
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

### 3. Frontend Setup
Install npm packages:
```bash
cd ../frontend
npm install
```

### 4. Running the Application
```bash
# Run database migrations and seed default personas
cd ../backend
alembic upgrade head
python app/db/seed.py

# Boot FastAPI server (Listens on port 8000)
uvicorn app.main:app --reload

# In a separate terminal, launch Next.js client
cd ../frontend
npm run dev
```

### 5. Running with Docker
To run the entire ecosystem locally inside a single production container layout:
```bash
# Start Docker compose
docker-compose up --build
```

---

## 🧬 API Endpoints

<details>
<summary>🔑 Authentication</summary>

| Method | Path | Authentication Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | No | Registers a new candidate account. |
| `POST` | `/api/v1/auth/login` | No | Verifies credentials and returns access JWT. |
</details>

<details>
<summary>👥 Personas</summary>

| Method | Path | Authentication Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/personas` | Yes | Lists available interviewer personas. |
| `POST` | `/api/v1/personas` | Yes | Creates a custom, user-defined persona. |
</details>

<details>
<summary>🎙️ Interviews</summary>

| Method | Path | Authentication Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interviews/start` | Yes | Initiates a session and yields the opening question. |
| `POST` | `/api/v1/interviews/{id}/message` | Yes | Appends candidate answer and returns AI follow-up. |
| `POST` | `/api/v1/interviews/{id}/complete` | Yes | Completes session and locks further messages. |
| `GET` | `/api/v1/interviews` | Yes | Lists all past interview sessions for the logged user. |
| `GET` | `/api/v1/interviews/{id}` | Yes | Fetches metadata and message turns for the session ID. |
</details>

<details>
<summary>📊 Evaluations & Reports</summary>

| Method | Path | Authentication Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/interviews/{id}/evaluate` | Yes | Calculates feedback scores. Persists to database. |
| `GET` | `/api/v1/interviews/{id}/evaluation` | Yes | Fetches evaluation dashboard details. |
| `GET` | `/api/v1/interviews/{id}/report` | Yes | Compiles downloadable markdown performance report. |
</details>

---

## ⚙️ Environment Variables

Copy `backend/.env.example` to `backend/.env`:

| Parameter | Purpose | Default / Sample |
| :--- | :--- | :--- |
| `DATABASE_URL` | SQLAlchemy Connection URL | `postgresql+psycopg://user:pass@host/dbname` |
| `GEMINI_API_KEY` | Upstream Gemini AI API Token | `AIzaSyD-your-api-key-here` |
| `JWT_SECRET` | Secret key used to sign JWT tokens | `secure-cryptographic-secret` |
| `JWT_ALGORITHM` | Token encryption algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Session validity duration (minutes) | `60` |
| `NEXT_PUBLIC_API_URL` | Frontend endpoint mapper | `/api/v1` |

---

## 🌀 Workflow

The following flowchart outlines the path candidates take during a mock technical interview:

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

- [ ] 🎙️ **Speech-to-Text Integration**: Allow users to speak their answers using audio recording streaming.
- [ ] 👥 **Community Personas**: Enable shared public user-created interviewer personas.
- [ ] 💻 **Interactive Code Sandbox**: Code editor panel for real-time coding simulations.

---

## 👥 Contributors

<p align="center">
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/logitechsoumili">
          <img src="https://placehold.co/100x100/A855F7/ffffff?text=Soumili" alt="Soumili Avatar" width="60" style="border-radius:50%;" /><br/>
          <sub><strong>Soumili Saha</strong></sub>
        </a><br/>
        💻 Project Architect
      </td>
      <td align="center">
        <a href="https://github.com/logitechsoumili/interviewverse-ai/graphs/contributors">
          <img src="https://placehold.co/100x100/4169E1/ffffff?text=Rupsha" alt="Rupsha Avatar" width="60" style="border-radius:50%;" /><br/>
          <sub><strong>Rupsha Debnath</strong></sub>
        </a><br/>
        ⚙️ DevOps & SRE
      </td>
    </tr>
  </table>
</p>

---

## 📄 License

This project is licensed under the **InterviewVerse AI Proprietary License**.

No permission is granted to copy, modify, redistribute, or commercially use this software without prior written consent from the copyright holders.

See the [LICENSE](LICENSE) file for details.
