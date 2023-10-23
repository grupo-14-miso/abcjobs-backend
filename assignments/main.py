from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import firebase_admin
from firebase_admin import credentials
from google.cloud import pubsub_v1
from google.oauth2 import service_account

from src.view.assignments_view import VistaPing, AssignmentsView, AssignmentSubmissionView, QuestionnaireView


app = Flask(__name__)


cred = credentials.Certificate("./firebase.json")
firebase_admin.initialize_app(cred)
credentials = service_account.Credentials.from_service_account_file("./firebase.json")
app.config['PROPAGATE_EXCEPTIONS'] = True

project_id = 'abc-jobs-miso'
topic_name = 'gradement-assigment'
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, topic_name)


api = Api(app)
api.add_resource(VistaPing, "/assignments/ping")
api.add_resource(AssignmentsView, "/assignments")
api.add_resource(AssignmentSubmissionView, "/assignments/<string:assignment_id>", resource_class_kwargs={'publisher': publisher, 'topic_path': topic_path})
api.add_resource(QuestionnaireView, "/assignments/questionnaire/<string:assignment_id>")



cors = CORS(app)
app_context = app.app_context()
app_context.push()
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)