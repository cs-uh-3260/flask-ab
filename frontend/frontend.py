from flask import Flask, render_template, request, make_response, session
import random
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

BACKEND_URL = environ.get("BACKEND_URL")
FRONTEND_PORT = environ.get("FRONTEND_PORT")


@app.route("/")
def home():
    # return render_template("index_a.html", backend_url=BACKEND_URL)
    # Comment out the above line and uncomment the following lines to enable A/B testing
    variant = request.cookies.get("ab_test_variant")
    if not variant:
        variant = random.choice(["a", "b"])
    template_name = f"index_{variant}.html"
    # make_response(...) wraps the HTML string from render_template in a Response object such that we can set cookies on it.
    response = make_response(render_template(template_name, backend_url=BACKEND_URL))
    # We are putting a max time of 2 minutes on this session cookie
    # here just to make it faster for the demo
    response.set_cookie("ab_test_variant", variant, max_age=60 * 2)
    return response


@app.route("/create_student")
def create_student():
    return render_template("create_student.html", backend_url=BACKEND_URL)


@app.route("/list_students")
def list_students():
    return render_template("list_students.html", backend_url=BACKEND_URL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONTEND_PORT, debug=True)
