import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials
from google.oauth2 import service_account

from src.view.company_view import VistaPing, CompanyView, OfferByCompanyView, EquipoByOfferView, OfferByIdView

app = Flask(__name__)

data = os.path.abspath(os.path.dirname(__file__)) + "/firebase.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)
credentials = service_account.Credentials.from_service_account_file(data)
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
api.add_resource(VistaPing, "/companies-get/ping")
api.add_resource(OfferByIdView, "/companies-get/offerById/<string:offer_id>")
api.add_resource(OfferByCompanyView, "/companies-get/offer/<string:company_id>")
api.add_resource(EquipoByOfferView, "/companies-get/equipo/<string:offer_id>")
api.add_resource(CompanyView, "/companies-get")



cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3007)
