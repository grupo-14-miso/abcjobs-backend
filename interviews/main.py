from coverage.annotate import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials
from flask_cors import CORS

from src.view.interview_view import VistaPing, VistaSelectionUser, VistaInterviewCompany, VistaInterview, VistaInterviewResult

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

CORS(app)

data = os.path.abspath(os.path.dirname(__file__)) + "/firebase.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)


api = Api(app)
api.add_resource(VistaPing, "/interviews/ping")
api.add_resource(VistaSelectionUser, "/interviews/pre-candidate")
api.add_resource(VistaInterviewCompany, "/interviews/offer/<string:id_offer>/pre")
api.add_resource(VistaInterview, "/interviews")
api.add_resource(VistaInterviewResult, "/interviews/<string:id_interview>")


cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
