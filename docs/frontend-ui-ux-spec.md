# Frontend UI/UX Specification

This specification outlines the visual design, typography, spacing tokens, component structures, and motion guidelines for the **InterviewVerse AI** platform.

---

## 1. Design Principles

* **Modern AI SaaS Aesthetic**: Dark-themed options, clean borders, glassmorphic card elements, subtle gradients, and highly contrastive interactive items.
* **Minimalist & Clean**: Content-first hierarchy. Interface elements fade away during active interviews to maximize focus.
* **Tactile Feedback**: Interactive controls scale slightly (`scale: 0.98`) when clicked and glow on focus.

---

## 2. Design Tokens (Tailwind System)

### Sleek Dark-Mode Color Palette
We configure a professional dark-slate color tokens list:

* **Background**: `hsl(224, 71%, 4%)` (Deep Space Dark)
* **Card/Surface**: `hsl(224, 71%, 7%)` (Slate Card Accent)
* **Border**: `hsl(224, 20%, 14%)` (Fine Muted Gray)
* **Primary (Accent)**: `hsl(263, 70%, 50%)` (Indigo Violet)
* **Secondary**: `hsl(190, 90%, 50%)` (Electric Cyan)
* **Destructive**: `hsl(0, 84%, 60%)` (Coral Red)

### Typography
* **Primary Sans**: `Inter`, System-Sans (Highly legible code & body text).
* **Display Sans**: `Outfit` or `Geist Sans` (Bold titles, metadata headers).
* **Font Weights**: regular (`400`), medium (`500`), semibold (`600`), and bold (`700`).

---

## 3. Motion & Micro-Animations (Framer Motion)

Animations enhance the interactive feeling of our interface:

### Route / Page Transitions
```typescript
export const pageTransition = {
  initial: { opacity: 0, y: 15 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -15 },
  transition: { duration: 0.3, ease: "easeOut" }
};
```

### Card Hover Effect (Persona Cards)
```typescript
export const cardHover = {
  hover: { 
    y: -4, 
    boxShadow: "0px 10px 30px rgba(124, 58, 237, 0.15)",
    borderColor: "rgba(124, 58, 237, 0.5)"
  }
};
```

### Active Interview Speech Waves (Micro-Animation)
* **Effect**: A pulse loops three small blue spheres on the audio/speech wave indicator:
  * Scale: oscillates between `1` and `1.6`.
  * Transition: `yoyo: Infinity`, `duration: 0.6s`.

---

## 4. Screen Wireframe Specifications

### A. Landing Page Layout
1. **Header**: Logo, product features, pricing links, registration CTA.
2. **Hero Section**: Huge headline ("Master your next technical interview with AI"), subheadline, glassmorphic video demo, and big main CTA button.
3. **Features Grid**: Three cards highlighting: real-time feedback, custom personas, and comprehensive reports.

### B. Dashboard Page Layout
```
+-------------------------------------------------------------+
|  [Logo] InterviewVerse-AI       (Search)        [User Icon]  |
+-------------------------------------------------------------+
|  (Sidebar)      |  Welcome back, John!                       |
|                 |  +-------------------------------------+  |
|  [x] Dashboard  |  |  Quick Start: Select a Platform     |  |
|  [ ] Personas   |  |  Interviewer Persona below...       |  |
|  [ ] History    |  +-------------------------------------+  |
|  [ ] Settings   |                                           |
|                 |  Active Sessions    Custom Personas        |
|                 |  [Card] SWE (Mid)   [Card] QA Lead (Senior)|
+-------------------+-----------------------------------------+
```

### C. Interview Screen Layout
* **Interviewer Panel (Top)**: Large card displaying selected Persona Avatar (e.g. Alex Rivera), role title, and animated pulse indicator signifying AI status.
* **Message History Pane (Middle)**: Chat bubble container with scroll auto-snapping. Candidate messages align right (Indigo bubbles); Interviewer messages align left (Dark Grey bubbles).
* **Input Area (Bottom)**: Multi-line text field, message characters count, timer overlay, and "Send" / "Complete Interview" buttons.

### D. Evaluation Screen Layout
* **Metrics Radar Chart (Left)**: Interactive SVG chart visualizing scores (Technical, Communication, Confidence).
* **Score Callouts (Right)**: Huge percentage scores with progress bars.
* **Feedback Tabs (Bottom)**: Toggle tabs display:
  * *Strengths* (green list items)
  * *Weaknesses* (red list items)
  * *Roadmap* (step-by-step roadmap items)
