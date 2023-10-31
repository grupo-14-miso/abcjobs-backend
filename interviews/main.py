from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials

from src.view.interview_view import VistaPing, VistaSelectionUser, VistaInterviewCompany

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

cred = credentials.Certificate('./firebase.json')
firebase_admin.initialize_app(cred)


api = Api(app)
api.add_resource(VistaPing, "/interviews/ping")
api.add_resource(VistaSelectionUser, "/interviews/pre-candidate")
api.add_resource(VistaInterviewCompany, "/interviews/offer/<string:id_offer>/pre")


cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3003)
