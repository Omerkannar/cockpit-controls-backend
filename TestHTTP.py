import threading
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory, request
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
from flask_cors import CORS
from datetime import datetime

# Global Data
app = Flask(__name__, template_folder='./swagger/templates')
CORS(app)

spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

# Data Definition
class StudentSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class StedentListSchema(Schema):
    list = fields.List(fields.Nested(StudentSchema))

studentList = [{"id":"3039", "name":"boris"},{"id":"2529", "name":"idan"}]

# Swagger Route Definition
@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', secure_filename(path))

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())

@app.route("/add_student", methods=["POST"])
def add_student():
    """Post add_student
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: StudentSchema
          """
    print('start -> add_student')
    if request.is_json:
        request_json = request.get_json()
        xxx = request_json["Data_Str_1"]
        print('finish -> add_student')
        return request_json, 201
    return {"Error": "Request must be JSON"}, 415

@app.get("/get_student_list")
def get_student_list():
    """Get Test List
        ---
        get:
            description: get_student_list
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: StedentListSchema
        """
    return jsonify(studentList)

#=======================================================================================================================
# Swagger Content
#=======================================================================================================================
with app.test_request_context():
    spec.path(view=add_student)
    spec.path(view=get_student_list)

def flask_run():
    print("Running RestAPI")
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    print('Start Code Python')
    flask_thread = threading.Thread(target=flask_run)
    flask_thread.start()
    flask_thread.join()

