from flask import Flask, request

from landing_page import landing_page
from overview import generate_overview_func
from sprint_generator import generate_sprint
from flask_cors import CORS, cross_origin
from generate_test_cases import generate_test_cases
from closing_document import generate_closing_doc_func

app = Flask(__name__)


def create_response(status, message, data, code):
    """Creates a response object with status, message, data, and HTTP status code."""
    return {"status": status, "message": message, "data": data}, code


def handle_request(func, *args, **kwargs):
    try:
        par = request.json if request.method == "POST" else request.args
        if request.method == "POST":
            print(f"{par}\n")
        return func(par, *args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")
        return create_response(False, f"Error: An error occurred {e}", {}, 400)


@app.route(f"/api//home_section", methods=["POST"])
@cross_origin()
def blog_script_route():
    """Handle the POST request to generate blog script"""
    return handle_request(landing_page)



@app.route("/api/generate-overview", methods=["POST"])
@cross_origin()
def generate_overview_route():
    if request.is_json:
        par = request.get_json()
        content = generate_overview_func(par.get("client_requirements"))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400


@app.route("/api/generate-sprint", methods=["POST"])
@cross_origin()
def generate_sprint_route():
    if request.is_json:
        par = request.get_json()
        content = generate_sprint(par.get("client_requirements"))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400


@app.route("/api/generate-testcases", methods=["POST"])
@cross_origin()
def generate_testcases_route():
    if request.is_json:
        par = request.get_json()
        content = generate_test_cases(par.get("client_requirements"))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400


@app.route("/api/generate-closing-document", methods=["POST"])
@cross_origin()
def generate_closing_document_route():
    if request.is_json:
        par = request.get_json()
        content = generate_closing_doc_func(par.get("client_requirements"))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400


if __name__ == "__main__":
    app.run(port=5001)
