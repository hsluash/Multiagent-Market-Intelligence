from google.cloud import firestore
from datetime import datetime, timedelta

db = firestore.Client()


def save_note(topic: str, content: str) -> str:
    """
    Save a structured research note to Firestore.

    Args:
        topic: The market topic this note is about.
        content: The note content to save (key insights, summary, etc).

    Returns:
        Confirmation message with the saved note ID.
    """
    if not topic or not content:
        return "Error: topic and content are required to save a note."

    doc_ref = db.collection("notes").add({
        "topic": topic,
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    })

    return f"Note saved successfully for topic '{topic}' (ID: {doc_ref[1].id})"


def save_task(title: str, description: str, due_date: str = "") -> str:
    """
    Save a follow-up action task to Firestore.

    Args:
        title: Short title of the task (e.g. 'Investigate funding trends').
        description: What needs to be done and why.
        due_date: Optional ISO date string (YYYY-MM-DD). Defaults to 7 days from now.

    Returns:
        Confirmation message with the saved task ID.
    """
    if not title or not description:
        return "Error: title and description are required to save a task."

    if not due_date:
        due_date = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")

    doc_ref = db.collection("tasks").add({
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    })

    return f"Task '{title}' saved (due: {due_date}, ID: {doc_ref[1].id})"


def get_schedule(topic: str) -> str:
    """
    Retrieve the scheduled research sessions and pending tasks for a topic.

    Args:
        topic: The market topic to look up scheduled sessions for.

    Returns:
        A summary of upcoming tasks and sessions for the topic.
    """
    if not topic:
        return "Error: topic is required."

    tasks = (
        db.collection("tasks")
        .where("status", "==", "pending")
        .order_by("due_date")
        .limit(5)
        .stream()
    )

    task_list = [doc.to_dict() for doc in tasks]

    if not task_list:
        return f"No scheduled tasks found. A follow-up research session has been noted for topic: '{topic}'."

    lines = [f"Upcoming tasks related to your research:"]
    for t in task_list:
        lines.append(f"- [{t.get('due_date', 'TBD')}] {t.get('title', '')}: {t.get('description', '')}")

    return "\n".join(lines)