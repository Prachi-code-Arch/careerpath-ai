# CareerPath AI
### Multi-Agent Career Coach for First-Generation Professionals in APAC
Built for Google Cloud Gen AI Academy Hackathon — APAC Edition

## Live Demo
- **Frontend:** https://careerpath-ai-2026.web.app
- **API:** https://careerpath-backend-66798922244.us-central1.run.app
- **Health check:** https://careerpath-backend-66798922244.us-central1.run.app/health

## The Problem
First-generation professionals in India and Southeast Asia navigate promotions,
salary negotiations, and career growth without mentors. CareerPath AI is their
always-available career manager.

## How It Works
User message → Orchestrator Agent (Gemini) → routes to 4 specialist agents → combined response saved to Firestore

## 4 Agents
- **Coach Agent** — promotion strategy, salary negotiation, APAC-aware coaching
- **Achievement Agent** — logs wins, generates review bullet points
- **Skillbuild Agent** — creates 4-week micro-task learning plans
- **Schedule Agent** — blocks calendar time for review prep

## Tech Stack
- Gemini 2.5 Flash via Vertex AI
- Cloud Firestore
- FastAPI on Cloud Run
- Firebase Hosting

## API Endpoints
- POST /chat — multi-agent chat
- POST /profile — create user profile
- GET /profile/{id} — get wins and goals
- GET /health — health check
