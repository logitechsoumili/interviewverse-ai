# Frontend API Integration Reference

This document maps all backend endpoints, defining authentication headers, payload interfaces, and integration notes for the frontend.

---

## 1. Global Setup

* **Base URL**: `/api/v1` (locally `http://localhost:8000/api/v1`)
* **Headers**: `Content-Type: application/json`
* **Authorization**: JWT Bearer token passed in headers for protected routes:
  `Authorization: Bearer <token>`

---

## 2. Authentication API

### POST `/api/v1/auth/register`
* **Purpose**: Register a new user.
* **Authentication**: None.
* **Request Body**:
  ```typescript
  interface RegisterRequest {
    email: string;
    full_name: string;
    password: string;
  }
  ```
* **Response Body (HTTP 201)**:
  ```typescript
  interface UserResponse {
    id: string; // UUID
    email: string;
    full_name: string;
    created_at: string; // ISO DateTime
  }
  ```

### POST `/api/v1/auth/login`
* **Purpose**: Authenticate credentials and retrieve JWT.
* **Authentication**: None.
* **Request Body**:
  ```typescript
  interface LoginRequest {
    email: string;
    password: string;
  }
  ```
* **Response Body (HTTP 200)**:
  ```typescript
  interface TokenResponse {
    access_token: string;
    token_type: string; // "bearer"
  }
  ```

### GET `/api/v1/users/me`
* **Purpose**: Retrieve current logged-in user profile.
* **Authentication**: Required.
* **Response Body (HTTP 200)**:
  ```typescript
  interface UserProfileResponse {
    id: string; // UUID
    email: string;
    full_name: string;
    created_at: string;
  }
  ```

---

## 3. Personas API

### GET `/api/v1/personas`
* **Purpose**: Retrieve available interviewer personas (platform defaults and custom owned).
* **Authentication**: Optional. If token is present, user-created custom personas are also included in the return list.
* **Response Body (HTTP 200)**:
  ```typescript
  interface Persona {
    id: string; // "hr_interviewer" or uuid
    name: string;
    role: string;
    description: string;
    interview_style: string;
    supported_difficulty_levels: string[];
    focus_areas: string[];
    system_context: string;
  }
  type PersonaList = Persona[];
  ```

### POST `/api/v1/personas`
* **Purpose**: Create a new custom persona.
* **Authentication**: Required.
* **Request Body**:
  ```typescript
  interface CreatePersonaRequest {
    id: string; // Unique alphanumeric string key
    name: string;
    role: string;
    description: string;
    interview_style: string;
    supported_difficulty_levels: string[];
    focus_areas: string[];
    system_context: string;
  }
  ```
* **Response Body (HTTP 201)**: `Persona` (Same as GET persona representation).

---

## 4. Interviews API

### POST `/api/v1/interviews/start`
* **Purpose**: Initialize a new interview simulation session and get the first question.
* **Authentication**: Required.
* **Request Body**:
  ```typescript
  interface StartInterviewRequest {
    persona_id: string; // Platform persona key or custom persona ID
    topics: string[];
    difficulty: 'junior' | 'mid' | 'senior';
  }
  ```
* **Response Body (HTTP 200)**:
  ```typescript
  interface StartInterviewResponse {
    interview_id: string; // UUID
    question: string;
    question_number: number; // 1
  }
  ```

### POST `/api/v1/interviews/{id}/message`
* **Purpose**: Submit user's answer to the current question and retrieve the next question.
* **Authentication**: Required.
* **Request Body**:
  ```typescript
  interface MessageRequest {
    message: string;
  }
  ```
* **Response Body (HTTP 200)**:
  ```typescript
  interface MessageResponse {
    question: string; // Next question or final feedback text
    question_number: number;
  }
  ```

### POST `/api/v1/interviews/{id}/complete`
* **Purpose**: Explicitly mark an active interview session as finished, closing it to further message submissions.
* **Authentication**: Required.
* **Response Body (HTTP 200)**:
  ```typescript
  interface CompleteInterviewResponse {
    status: "completed";
  }
  ```

### GET `/api/v1/interviews`
* **Purpose**: List user's historical interview sessions.
* **Authentication**: Required.
* **Response Body (HTTP 200)**:
  ```typescript
  interface InterviewSessionMetadata {
    id: string; // UUID
    persona_id: string;
    topics: string[];
    difficulty: string;
    status: 'active' | 'completed';
    created_at: string;
  }
  type InterviewListResponse = InterviewSessionMetadata[];
  ```

---

## 5. Evaluations & Reports API

### POST `/api/v1/interviews/{id}/evaluate`
* **Purpose**: Trigger evaluation generation for a completed interview session.
* **Authentication**: Required.
* **Response Body (HTTP 200)**:
  ```typescript
  interface Scores {
    technical_accuracy: number; // 0-100
    communication: number;      // 0-100
    confidence: number;         // 0-100
    overall: number;            // 0-100
  }
  interface Feedback {
    strengths: string[];
    weaknesses: string[];
    roadmap: string[];
  }
  interface EvaluationResponse {
    id: string;
    interview_id: string;
    persona_id: string;
    scores: Scores;
    feedback: Feedback;
    created_at: string;
  }
  ```

### GET `/api/v1/interviews/{id}/evaluation`
* **Purpose**: Retrieve existing evaluation results.
* **Authentication**: Required.
* **Response Body (HTTP 200)**: `EvaluationResponse` (same structure as above).

### GET `/api/v1/interviews/{id}/report`
* **Purpose**: Generate and retrieve the full summary candidate report in raw markdown layout.
* **Authentication**: Required.
* **Response Body (HTTP 200)**:
  ```typescript
  interface ReportResponse {
    id: string;
    interview_id: string;
    persona_id: string;
    markdown_content: string; // Complete markdown file output
    created_at: string;
  }
  ```
