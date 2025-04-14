from functools import wraps
from flask import request
from ab_testing.utils import get_session_id
from db import ab_test

def ab_test_backend(experiment_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            session_id = get_session_id()
            variant = request.cookies.get(experiment_name, "unknown")
            ab_test.log_ab_test_event(session_id, variant, "list_students_viewed")

            return response
        return wrapper
    return decorator
