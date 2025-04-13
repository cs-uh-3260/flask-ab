from datetime import datetime, timezone
from .db import get_db


def log_ab_test_event(session_id, variant, event_type):
    db = get_db()
    db.ab_test_logs.insert_one(
        {
            "session_id": session_id,
            "variant": variant,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc),
        }
    )
