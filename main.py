import logging
import os
import google.cloud.logging
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.coordinator import coordinator_agent
from tools.storage_tools import save_report, retrieve_reports

# Cloud Logging (safe fallback to standard logging if not on GCP)
try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

# ADK Runner setup
session_service = InMemorySessionService()
runner = Runner(
    agent=coordinator_agent,
    app_name="market_intelligence",
    session_service=session_service
)


class Request(BaseModel):
    topic: str

@app.get("/")
def root():
    return {"message": "Market Intelligence API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate(req: Request):
    topic = req.topic

    session = await session_service.create_session(
        app_name="market_intelligence",
        user_id="api_user"
    )

    # session = session_service.create_session(
    # app_name="market_intelligence",
    # user_id="api_user"
    # )

    # # Fix for coroutine edge cases
    # if hasattr(session, "__await__"):
    #     session = await session

    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=topic)]
    )

    result_text = ""
    for event in runner.run(
        user_id="api_user",
        session_id=session.id,
        new_message=message
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    result_text += part.text

    # try:
    #     parsed = json.loads(result_text)
    # except:
    #     parsed = {
    #         "trends": [],
    #         "opportunities": [],
    #         "risks": []
    #     }

    save_report(topic, result_text)

    return {
        "topic": topic,
        "report": result_text
    }


@app.get("/history/{topic}")
def history(topic: str):
    reports = retrieve_reports(topic)

    return {
        "topic": topic,
        "history_count": len(reports),
        "reports": reports
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)