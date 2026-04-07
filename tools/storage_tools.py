from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def save_report(topic: str, report: str):
    db.collection("reports").add({
        "topic": topic,
        "report": report,
        "timestamp": datetime.utcnow().isoformat()
    })

def retrieve_reports(topic: str):
    docs = (
        db.collection("reports")
        .where("topic", "==", topic)
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .stream()
    )
    return [doc.to_dict() for doc in docs]