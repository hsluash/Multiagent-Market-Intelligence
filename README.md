[![Watch Demo](https://youtu.be/7_3Gv_o84Xc)](https://youtu.be/7_3Gv_o84Xc)
# 📊 Multiagent Market Intelligence System

> A multi-agent AI system that researches any market topic end-to-end — from gathering live data and generating a structured business report, to automatically creating follow-up tasks, saving notes, and scheduling next steps — so users go from **research to action in a single request**.

Built with **Google ADK**, **Gemini**, **FastAPI**, **Firestore**, and deployed on **Google Cloud Run**.

---

## 🎯 Project Goal

Most market research tools stop at the report. This system goes further.

You give it a topic like *"AI in healthcare"*. It doesn't just write a report — it **acts on it**. It saves the key insights as a note, creates specific follow-up tasks with due dates, and retrieves your schedule of pending actions. The entire workflow — research, analysis, reporting, and task planning — runs automatically through a coordinated pipeline of specialized AI agents.

This demonstrates a real-world agentic workflow: multiple agents collaborating, multiple tools being called, structured data being stored and retrieved, all exposed as a deployable API.

---

## 🏗️ Architecture

```
User Request: "AI in healthcare"
          │
          ▼
    FastAPI (main.py)
          │
          ▼
  ┌─────────────────────────────────────────────────┐
  │         SequentialAgent (coordinator)            │
  │                                                  │
  │  1. data_agent      → market context (tool)      │
  │         ↓                                        │
  │  2. research_agent  → live web research          │
  │         ↓           (google_search built-in)     │
  │  3. analyzer_agent  → structured JSON insights   │
  │         ↓                                        │
  │  4. report_agent    → professional report        │
  │         ↓                                        │
  │  5. action_agent    → saves note + tasks +       │
  │                        retrieves schedule        │
  └─────────────────────────────────────────────────┘
          │
          ▼
    Firestore DB
    (reports, notes, tasks collections)
          │
          ▼
    Streamlit UI (ui.py)
```

---

## 🤖 Agents

| Agent | Role | Tools Used |
|---|---|---|
| `data_agent` | Generates initial market context for the topic | `get_market_trends` (function tool) |
| `research_agent` | Enriches context with live web data | `google_search` (ADK built-in) |
| `analyzer_agent` | Extracts structured JSON: trends, opportunities, risks | None — pure LLM reasoning |
| `report_agent` | Converts JSON into a professional business report | None — pure LLM generation |
| `action_agent` | Saves note, creates follow-up tasks, retrieves schedule | `save_note`, `save_task`, `get_schedule` (function tools) |

**Coordinator**: `SequentialAgent` — runs all 5 agents in order, passing each output as input to the next.

---

## 🛠️ Tools

### Function Tools (custom, Firestore-backed)
| Tool | What it does | Firestore collection |
|---|---|---|
| `get_market_trends(topic)` | Returns base market context for a topic | — |
| `save_note(topic, content)` | Saves key insights as a structured note | `notes` |
| `save_task(title, description, due_date)` | Creates a follow-up action task | `tasks` |
| `get_schedule(topic)` | Retrieves pending tasks ordered by due date | `tasks` |

### Built-in ADK Tools
| Tool | What it does |
|---|---|
| `google_search` | Live web search grounding for `research_agent` |

> **Note on MCP**: ADK's `McpToolset` (for connecting to external MCP servers like Atlassian or GitHub) is not needed here. Custom Python functions are the correct ADK pattern for Firestore-backed tools. `google_search` is an ADK built-in — no external server required. One important ADK constraint: `google_search` must be the only tool in an agent — it cannot share an agent with other tools, which is why `research_agent` and `action_agent` are separate.

---

## 🗂️ Project Structure

```
.
├── main.py                    # FastAPI — API endpoints + ADK Runner
├── ui.py                      # Streamlit frontend
├── config.py                  # Env config
├── requirements.txt
├── Dockerfile
├── .env                       
│
├── agents/
│   ├── coordinator.py         # SequentialAgent wiring all 5 agents
│   ├── data_agent.py          # Market context via tool
│   ├── research_agent.py      # Live web research via google_search
│   ├── analyzer_agent.py      # JSON insight extraction
│   ├── report_agent.py        # Business report generation
│   └── action_agent.py        # Tasks, notes, schedule
│
└── tools/
    ├── market_tools.py        # get_market_trends()
    ├── action_tools.py        # save_note(), save_task(), get_schedule()
    └── storage_tools.py       # save_report(), retrieve_reports() for API
```

---

## API Endpoints

### `POST /generate`
Run the full 5-agent pipeline for a topic.

```bash
curl -X POST https://YOUR-URL/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "AI in healthcare"}'
```

Response:
```json
{
  "topic": "AI in healthcare",
  "report": "## Market Intelligence Report\n..."
}
```

### `GET /history/{topic}`
Retrieve previously generated reports from Firestore.

```bash
curl https://YOUR-URL/history/AI%20in%20healthcare
```

### `GET /health`
Health check for Cloud Run.

---

## ⚙️ Local Setup

```bash
git clone https://github.com/hsluash/Multiagent-Market-Intelligence.git
cd Multiagent-Market-Intelligence
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

Edit `.env` with literal values:
```env
GOOGLE_GENAI_USE_VERTEXAI=1
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
SA_NAME=healthcare-agent
SERVICE_ACCOUNT=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
MODEL=gemini-2.5-flash
```

Run locally:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
# In a second terminal:
streamlit run ui.py
```
## Results

**Report**: Can be viewed on the streamlit UI and also in the firestore (in GCP)
**Notes & Tasks**: Can be found in the firestore based on corresponding topic

---

## 🚀 Deploy to Cloud Run

```bash
# 1. Enable services
gcloud services enable run.googleapis.com firestore.googleapis.com aiplatform.googleapis.com

# 2. Create Firestore
gcloud firestore databases create --location=us-central1

# 3. Grant IAM permissions
```
gcloud auth application-default login

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/datastore.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

# 4. Build and Deploy — explicit --port 8080 is required
gcloud run deploy market-intelligence \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port=8080 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=1,MODEL=gemini-2.5-flash

---

## 🔮 Future Roadmap

| Phase | Change | Agent / File to modify |
|---|---|---|
| Phase 2 | Replace mock `get_market_trends` with live web scraping | `data_agent` + `tools/market_tools.py` |
| Phase 3 | Connect real MCP servers (Slack, Google Calendar) via `McpToolset` | `action_agent` |
| Phase 4 | Add `sentiment_agent` between research and analyzer | New agent + `coordinator.py` |
| Phase 5 | Firestore-backed sessions for stateful multi-turn conversations | `main.py` |

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `google-adk` | Agent framework — SequentialAgent, Runner, built-in tools |
| `fastapi` + `uvicorn` | REST API server |
| `google-cloud-firestore` | Reports, notes, tasks storage |
| `google-cloud-aiplatform` | Vertex AI / Gemini model access |
| `google-cloud-logging` | Structured logging on Cloud Run |
| `python-dotenv` | Local env var loading |
| `streamlit` + `requests` | Frontend UI |
