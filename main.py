import threading
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory, request
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, jsonify
from flask_cors import CORS
from array import array
from datetime import datetime
import json
import threading
import time
import random

#=======================================================================================================================
# Global Data
#=======================================================================================================================
app = Flask(__name__, template_folder='./swagger/templates')
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

fuel_increase_or_decrease = 1

#=======================================================================================================================
# Data Definition
#=======================================================================================================================
#
# CMDS Panel Data List
#
_CMDS_Panel_Data_List = [{"RWR_SWITCH": "True", "JMR_SWITCH": "True", "MWS_SWITCH": "True",
                          "SWITCH_01": "True", "SWITCH_02": "True", "SWITCH_CH": "True",
                          "SWITCH_FL": "True", "SWITCH_JETT": "True", "KNOB_PRGM": "bit",
                          "KNOB_MODE": "off", "STATUS_DISPENSE": "True", "STATUS_READY": "True",
                          "STATUS_NO": "True", "STATUS_NO_GO": "True", "STATUS_GO": "True",
                          "CH_TEN": "True", "CH_ONE": "True", "EPU_FUEL_LEVEL": "0"
                          }]

#
# Interior Light Panel
#
_InteriorLight_Panel_Data_List = [{"NORMLTG_LIGHT": "center"}]

#=======================================================================================================================
# Data Definition
#=======================================================================================================================
class CMDS_Schema(Schema):
    RWR_SWITCH = fields.Str()
    JMR_SWITCH = fields.Str()
    MWS_SWITCH = fields.Str()
    SWITCH_01 = fields.Str()
    SWITCH_02 = fields.Str()
    SWITCH_CH = fields.Str()
    SWITCH_FL = fields.Str()
    SWITCH_JETT = fields.Str()
    KNOB_PRGM = fields.Str()
    KNOB_MODE = fields.Str()
    STATUS_DISPENSE = fields.Str()
    STATUS_READY = fields.Str()
    STATUS_NO = fields.Str()
    STATUS_NO_GO = fields.Str()
    STATUS_GO = fields.Str()
    CH_TEN = fields.Str()
    CH_ONE = fields.Str()

class CMDS_List_Schema(Schema):
    list = fields.List(fields.Nested(CMDS_Schema))

class InteriorLight_Schema(Schema):
    NORMLTG_LIGHT = fields.Str()

class InteriorLight_List_Schema(Schema):
    list = fields.List(fields.Nested(InteriorLight_Schema))

#=======================================================================================================================
# Swagger Route Definition
#=======================================================================================================================
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

#=======================================================================================================================
# setCMDSPanelData
#=======================================================================================================================
@app.route("/setInteriorLightPanelData", methods=["POST"])
def setInteriorLightPanelData():
    """Post setInteriorLightPanelData
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: InteriorLight_Schema
          """
    print('start -> setInteriorLightPanelData')
    if request.is_json:

        request_json = request.get_json()

        NORMLTG_LIGHT_VALUE = request_json["NORMLTG_LIGHT"]

        _InteriorLight_Panel_Data_List[0]["NORMLTG_LIGHT"] = NORMLTG_LIGHT_VALUE

        print(request_json)
        print('finish -> setInteriorLightPanelData')
        return "success set Set Interior Light Panel Data", 200
    return {"Error": "Request must be JSON"}, 415

##################################################################
# getCMDSPanelData
##################################################################
@app.get("/getInteriorLightPanelData")
def getInteriorLightPanelData():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: InteriorLight_Schema
        """
    print('### get -> getInteriorLightPanelData')
    print(_InteriorLight_Panel_Data_List[0])
    return jsonify(_InteriorLight_Panel_Data_List[0])

#=======================================================================================================================
# setCMDSPanelData
#=======================================================================================================================
@app.route("/setCMDSPanelData", methods=["POST"])
def setCMDSPanelData():
    """Post registerData
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: CMDS_Schema
          """
    print('start -> setCMDSPanelData')
    if request.is_json:

        request_json = request.get_json()

        RWR_SWITCH_VALUE = request_json["RWR_SWITCH"]
        JMR_SWITCH_VALUE = request_json['JMR_SWITCH']
        MWS_SWITCH_VALUE = request_json["MWS_SWITCH"]
        SWITCH_01_VALUE = request_json["SWITCH_01"]
        SWITCH_02_VALUE = request_json["SWITCH_02"]
        SWITCH_CH_VALUE = request_json["SWITCH_CH"]
        SWITCH_FL_VALUE = request_json["SWITCH_FL"]
        SWITCH_JETT_VALUE = request_json["SWITCH_JETT"]
        KNOB_PRGM_VALUE = request_json["KNOB_PRGM"]
        KNOB_MODE_VALUE = request_json["KNOB_MODE"]
        #CH_TEN_VALUE = request_json["CH_TEN"]
        #CH_ONE_VALUE = request_json["CH_ONE"]

        _CMDS_Panel_Data_List[0]["RWR_SWITCH"] = RWR_SWITCH_VALUE
        _CMDS_Panel_Data_List[0]["JMR_SWITCH"] = JMR_SWITCH_VALUE
        _CMDS_Panel_Data_List[0]["MWS_SWITCH"] = MWS_SWITCH_VALUE
        _CMDS_Panel_Data_List[0]["SWITCH_01"] = SWITCH_01_VALUE
        _CMDS_Panel_Data_List[0]["SWITCH_02"] = SWITCH_02_VALUE
        _CMDS_Panel_Data_List[0]["SWITCH_CH"] = SWITCH_CH_VALUE
        _CMDS_Panel_Data_List[0]["SWITCH_FL"] = SWITCH_FL_VALUE
        _CMDS_Panel_Data_List[0]["SWITCH_JETT"] = SWITCH_JETT_VALUE
        _CMDS_Panel_Data_List[0]["KNOB_PRGM"] = KNOB_PRGM_VALUE
        _CMDS_Panel_Data_List[0]["KNOB_MODE"] = KNOB_MODE_VALUE
        #_CMDS_Panel_Data_List[0]["CH_TEN"] = str(CH_TEN_VALUE)
        #_CMDS_Panel_Data_List[0]["CH_ONE"] = str(CH_ONE_VALUE)

        print(request_json)
        print('finish -> setCMDSPanelData')
        return "success set CMDS Panel Data", 200
    return {"Error": "Request must be JSON"}, 415

##################################################################
# getCMDSPanelData
##################################################################
@app.get("/getCMDSPanelData")
def getCMDSPanelData():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: CMDS_Schema
        """
    print('### get -> getCMDSPanelData')
    global fuel_increase_or_decrease
    if fuel_increase_or_decrease == 1:
        _CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL'] = str(int(_CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL']) + 1)
        if _CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL'] == '100':
            _CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL'] = '100'
            fuel_increase_or_decrease = -1
    else:
        _CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL'] = str(int(_CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL']) - 1)
        if _CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL'] == '0':
            _CMDS_Panel_Data_List[0]['EPU_FUEL_LEVEL'] = '0'
            fuel_increase_or_decrease = 1

    print(_CMDS_Panel_Data_List[0])
    return jsonify(_CMDS_Panel_Data_List[0])

##################################################################
# getCMDSPanelDataList
##################################################################
@app.get("/getCMDSPanelDataList")
def getCMDSPanelDataList():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: CMDS_List_Schema
        """
    print('start -> getData')
    return jsonify(_CMDS_Panel_Data_List)

# Define a function that will be executed in the new thread
def internal_thread_function():
    while(True):
        time.sleep(10)

#=======================================================================================================================
# Swagger Content
#=======================================================================================================================
with app.test_request_context():
    spec.path(view=setCMDSPanelData)
    spec.path(view=getCMDSPanelData)
    spec.path(view=getCMDSPanelDataList)
    spec.path(view=setInteriorLightPanelData)
    spec.path(view=getInteriorLightPanelData)
def flask_run():
    print("Running RestAPI")
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    print('ATH Flight Data Python Server Started ...')

    internal_thread = threading.Thread(target=internal_thread_function)
    flask_thread = threading.Thread(target=flask_run)

    internal_thread.start()
    flask_thread.start()

    internal_thread.join()
    flask_thread.join()


