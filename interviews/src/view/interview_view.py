from flask_restful import Resource
from google.cloud import datastore
from flask import request

pre_interview_domain = 'pre_interview'

class VistaPing(Resource): 
    def get(self):
        return "Pong"



class VistaSelectionUser(Resource):
    def post(self):
        data = request.get_json()
        client = datastore.Client()

        # Create a new Datastore entity for the profile
        key = client.key(pre_interview_domain)
        new_pre_interview_request = datastore.Entity(key=key)
        new_pre_interview_request.update({
            'id_company': data['id_company'],
            'id_offer': data['id_offer'],
            'id_candidate':data['id_candidate']
        })

        # Save the entity to Datastore
        client.put(new_pre_interview_request)
        
        return str(key.id)
