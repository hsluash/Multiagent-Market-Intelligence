from fastapi import FastAPI
from pydantic import BaseModel

import logging
import google.cloud.logging

from agents.coordinator import coordinator_agent
from tools.storage_tools import save_report, retrieve_reports

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

app = FastAPI()


class Request(BaseModel):
    topic: str


@app.post("/generate")
def generate(req: Request):
    topic = req.topic

    result = coordinator_agent.run(topic)

    save_report(topic, str(result))

    return {
        "topic": topic,
        "report": result
    }


@app.get("/history/{topic}")
def history(topic: str):
    reports = retrieve_reports(topic)

    return {
        "topic": topic,
        "history_count": len(reports),
        "reports": reports
    }