from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def save_report(topic: str, report: str):
    if not topic or not report:
        return "Nothing to save"
    db.collection("reports").add({
        "topic": topic,
        "report": report,
        "timestamp": datetime.utcnow().isoformat()
    })

def retrieve_reports(topic: str):
    docs = (
        db.collection("reports")
        .where("topic", "==", topic)
        .stream()
    )
    results = [doc.to_dict() for doc in docs]
    # Sort in Python to avoid requiring a Firestore composite index
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return results