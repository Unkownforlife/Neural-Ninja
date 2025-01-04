from flask import Flask, request
from overview import generate_overview_func
from sprint_generator import generate_sprint
from flask_cors import CORS, cross_origin
from generate_test_cases import generate_test_cases
from closing_document import generate_closing_doc_func

app = Flask(__name__)


@app.route("/api/generate-overview", methods=['POST'])
@cross_origin()
def generate_overview_route():
    if request.is_json:
        par = request.get_json()
        content = generate_overview_func(par.get('client_requirements'))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400
    

@app.route("/api/generate-sprint", methods=['POST'])
@cross_origin()
def generate_sprint_route():
    if request.is_json:
        par = request.get_json()
        content = generate_sprint(par.get('client_requirements'))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400


@app.route("/api/generate-testcases", methods=['POST'])
@cross_origin()
def generate_testcases_route():
    if request.is_json:
        par = request.get_json()
        content = generate_test_cases(par.get('client_requirements'))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400


@app.route("/api/generate-closing-document", methods=['POST'])
@cross_origin()
def generate_closing_document_route():
    if request.is_json:
        par = request.get_json()
        content = generate_closing_doc_func(par.get('client_requirements'))
        return {"status": "success", "data": content}, 200
    else:
        return {"status": "error", "message": "Invalid JSON payload"}, 400
    



if __name__ == '__main__':  
   app.run()  
