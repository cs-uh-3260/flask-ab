from functools import wraps
from ab_testing.utils import get_or_assign_cookie_variant

def ab_test_frontend(experiment_name, variants):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            variant = get_or_assign_cookie_variant(experiment_name, variants)

            # Call the original function, i.e. the wrapped function
            response = func(*args, variant=variant, **kwargs)
            # We still have to set the cookie's value, i.e. the variant
            # Also, note that we set the cookie's max_age to 5 seconds to quickly check different variants
            # Change this to a longer duration accordingly
            response.set_cookie("landing_page", variant, max_age=5)
            return response
        return wrapper
    return decorator
