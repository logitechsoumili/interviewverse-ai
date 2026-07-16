# Frontend Implementation Roadmap

This document outlines the phased roadmap for building, polished-design tuning, and production-hardening the **InterviewVerse AI** frontend application.

---

## Phase 1: Project Setup (Milestone 1)
* **Goal**: Establish the Next.js workspace structure, base themes, and validation utilities.
* **Tasks**:
  * Scaffold Next.js 15 app using standard script configurations.
  * Install dependencies: Axios, TanStack Query, Zustand, Tailwind, shadcn/ui primitives.
  * Configure Tailwind with theme color design tokens.
  * Setup HTTP client interceptors.
* **Testing Requirements**: Smoke test check ensuring compiling succeeds and Base layouts compile without console warnings.
* **Completion Criteria**: App compiles, routing to `/` works, and base theme styles load correctly.

---

## Phase 2: Authentication Integration (Milestone 2)
* **Goal**: Implement secure user registration, token acquisition, and route protection.
* **Components**: `LoginForm`, `RegisterForm`, `UserAvatar`.
* **Pages**: `/login`, `/register`.
* **API Integrations**: `POST /auth/register`, `POST /auth/login`, `GET /users/me`.
* **Testing Requirements**:
  * Verify token validation intercepts.
  * Test JWT expiration redirects.
  * Check validation errors for invalid emails or missing credentials.
* **Completion Criteria**: A user can register, log in, view their email profile, and get redirected away from authenticated pages if unauthorized.

---

## Phase 3: Dashboard & History Layout (Milestone 3)
* **Goal**: Construct the primary container layouts and list interview history.
* **Components**: `Sidebar`, `Header`, `SessionMetadataCard`, `HistoryTable`.
* **Pages**: `/dashboard`, `/history`.
* **API Integrations**: `GET /interviews` (session list query).
* **Testing Requirements**:
  * Mock API lists and verify loading skeletons display correctly.
  * Verify responsive panel navigation scales to tablet and mobile screens.
* **Completion Criteria**: Dashboard renders user metadata and historical list items.

---

## Phase 4: Persona Library & Creation Builder (Milestone 4)
* **Goal**: Enable candidates to view default personas and register custom ones.
* **Components**: `PersonaGrid`, `PersonaCard`, `CreatePersonaDialog` / Form.
* **Pages**: `/personas`.
* **API Integrations**: `GET /personas`, `POST /personas`.
* **Testing Requirements**:
  * Verify that creating a custom persona invalidates `personas` query list and refetches.
  * Confirm that custom input validation boundaries correctly reject empty forms.
* **Completion Criteria**: Custom personas can be created and show up immediately in the grid library.

---

## Phase 5: Active Interview Simulation Sandbox (Milestone 5)
* **Goal**: Construct the primary interactive messaging chat and complete interviews.
* **Components**: `ChatFeed`, `MessageBubble`, `AnswerInput`, `Timer`, `CompleteDialog`.
* **Pages**: `/interviews/[id]`.
* **API Integrations**: `POST /interviews/start`, `POST /interviews/{id}/message`, `POST /interviews/{id}/complete`.
* **Testing Requirements**:
  * Verify turn loops process and scroll containers snap to the bottom of the feed.
  * Verify that closing/completing session disables further message inputs.
  * Test user text recovery on generation failure.
* **Completion Criteria**: Candidates can start, exchange messages, and complete interviews.

---

## Phase 6: Assessment Evaluations & Reports (Milestone 6)
* **Goal**: Render performance charts, feedback, and markdown reports.
* **Components**: `RadarScoreChart`, `ScoreProgressRing`, `FeedbackTabs`, `MarkdownReportViewer`.
* **Pages**: `/interviews/[id]/evaluation`, `/interviews/[id]/report`.
* **API Integrations**: `POST /interviews/{id}/evaluate`, `GET /interviews/{id}/evaluation`, `GET /interviews/{id}/report`.
* **Testing Requirements**: Verify score values translate to visual chart coordinates.
* **Completion Criteria**: Score parameters, qualitatively separated feedback logs, and final reports render successfully.

---

## Phase 7: Polish & Micro-Animations (Milestone 7)
* **Goal**: Implement premium visual enhancements.
* **Tasks**:
  * Add Framer Motion route transitions.
  * Setup hover states and focus animations.
  * Setup speech pulse waves during AI wait cycles.
* **Testing Requirements**: Confirm smooth frames per second (60fps) during UI animations.

---

## Phase 8: Hardening & Production Ready Review (Milestone 8)
* **Goal**: Final audit checks and performance improvements.
* **Tasks**:
  * Run lighthouse audit for performance, accessibility, best practices, and SEO.
  * Final TypeScript checking (`tsc --noEmit`).
  * Verify error boundaries handle failures.
* **Completion Criteria**: Next.js production build completes without errors, and bundle size is optimized.
