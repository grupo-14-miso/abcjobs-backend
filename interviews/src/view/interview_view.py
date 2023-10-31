from flask_restful import Resource
from google.cloud import datastore
from flask import request

pre_interview_domain = 'pre_interview'
candidates_domain ='candidates'

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
            'id_candidate':data['id_candidate'],
            'status':'available'
        })

        # Save the entity to Datastore
        client.put(new_pre_interview_request)
        
        return str(key.id)

class VistaInterviewCompany(Resource):
    def get(self, id_offer):
        #company_id = request.args.get('id_company')

        client = datastore.Client()

        # Query all pre_interview entities
        pre_interview_query = client.query(kind=pre_interview_domain).add_filter('id_offer', '=', id_offer)
        pre_interview_results = list(pre_interview_query.fetch())

        all_pre_interview_details = []

        print(pre_interview_results)

        for pre_interview_entity in pre_interview_results:
            # Extract IDs for company, offer, and candidate
            candidate_id = pre_interview_entity['id_candidate']

            key_candidate = client.key(candidates_domain, int(candidate_id))

            candidate = client.get(key_candidate)


            # Combine the results
            pre_interview_details = {
                'pre_interview': pre_interview_entity,
                'candidate': candidate if candidate else None,
            }

            all_pre_interview_details.append(pre_interview_details)

        return all_pre_interview_details