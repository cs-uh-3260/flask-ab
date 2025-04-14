from ab_testing.ab_testing import ab_test_frontend
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
@ab_test_frontend("landing_page", ["a", "b", "c"])
def home(variant):
    template_name = f"index_{variant}.html"
    
    # make_response(...) wraps the HTML string from render_template in a Response object such that we can set cookies on it.
    response = make_response(render_template(template_name, backend_url=BACKEND_URL))
    
    return response


@app.route("/create_student")
def create_student():
    return render_template("create_student.html", backend_url=BACKEND_URL)


@app.route("/list_students")
def list_students():
    return render_template("list_students.html", backend_url=BACKEND_URL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONTEND_PORT, debug=True)
