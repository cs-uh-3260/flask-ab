import random
from flask import session, request


def get_or_assign_cookie_variant(experiment_name, variants):
    variant = request.cookies.get(experiment_name)
    if not variant:
        variant = random.choice(variants)
    return variant
