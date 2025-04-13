from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from flask import jsonify, request, session
from bson.json_util import dumps
from db import students
from db import ab_test
import uuid

api = Namespace("students", description="Endpoint for students")

STUDENT_CREATE_FLDS = api.model(
    "AddNewStudentEntry",
    {
        students.NAME: fields.String,
        students.EMAIL: fields.String,
        students.SENIORITY: fields.String,
    },
)


# this is a helper function to get the session id
# you may put this in a separate file if you want
def get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]


@api.route("/")
class StudentList(Resource):

    @api.doc(
        params={
            "name": "Filter student list by student name (partial matches allowed)",
            "seniority": "Filter student list by student seniority (Exact seniority match)",
        }
    )
    def get(self):
        name = request.args.get("name")
        seniority = request.args.get("seniority")
        student_list = students.get_students(name, seniority)

        # Uncomment following lines to enable logging of A/B test events
        # log AB test event
        variant = request.cookies.get("ab_test_variant", "unknown")
        session_id = get_session_id()
        ab_test.log_ab_test_event(session_id, variant, "list_students_viewed")

        return student_list, HTTPStatus.OK

    @api.expect(STUDENT_CREATE_FLDS)
    def post(self):
        name = request.json.get(students.NAME)
        seniority = request.json.get(students.SENIORITY)
        email = request.json.get(students.EMAIL)
        student_id = students.create_student(name, email, seniority)
        print(f"Created student with id: {student_id}")
        return "Student created", HTTPStatus.OK


@api.route("/<email>")
@api.param("email", "Student email to use for lookup")
@api.response(404, "Student not found")
@api.response(HTTPStatus.OK, "Success")
@api.response(HTTPStatus.NOT_ACCEPTABLE, "Not acceptable")
class Student(Resource):

    @api.doc("Get a specific student, identified by email")
    def get(self, email):
        student = students.get_student_by_email(email)

        if student is None:
            return "Student not found", HTTPStatus.NOT_FOUND

        return student, HTTPStatus.OK

    @api.expect(STUDENT_CREATE_FLDS)
    @api.doc("Update a specific student, identified by email")
    def put(self, email):

        name = request.json.get(students.NAME)
        seniority = request.json.get(students.SENIORITY)
        new_email = request.json.get(students.EMAIL)

        updated_student = students.update_student(email, name, new_email, seniority)

        if updated_student is None:
            return "Student not found", HTTPStatus.NOT_FOUND

        return "Student updated", HTTPStatus.OK

    def delete(self, email):
        deleted_student = students.delete_student(email)
        if deleted_student == 0:
            return "Student not found", HTTPStatus.NOT_FOUND
        return "Student deleted", HTTPStatus.OK
