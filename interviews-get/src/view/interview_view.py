from flask_restful import Resource
from google.cloud import datastore
from flask import request
from flask import jsonify

pre_interview_domain = 'pre_interview'
candidates_domain = 'candidates'
interviews_domain = 'interviews'
offers_data_domain = 'offers-data'
companies_data_domain = 'companies-data'


class VistaPing(Resource):
    def get(self):
        return "Pong"


class VistaInterviewCompany(Resource):
    def get(self, id_offer):

        client = datastore.Client()

        # Query all pre_interview entities
        pre_interview_query = client.query(kind=pre_interview_domain).add_filter('id_offer', '=', id_offer)
        pre_interview_results = list(pre_interview_query.fetch())

        all_pre_interview_details = []

        for pre_interview_entity in pre_interview_results:
            # Extract IDs for company, offer, and candidate
            candidate_id = pre_interview_entity['id_candidate']

            key_candidate = client.key(candidates_domain, int(candidate_id))

            candidate = client.get(key_candidate)
            # Combine the results
            pre_interview_details = {
                'key': pre_interview_entity.key.path[-1],
                'pre_interview': pre_interview_entity,
                'candidate': candidate if candidate else None,
            }
            
            if 'candidate' in pre_interview_details and 'password_hash' in pre_interview_details['candidate']:
                pre_interview_details['candidate']['password_hash'] = ""
                pre_interview_details['candidate']['salt'] = ""

            all_pre_interview_details.append(pre_interview_details)
        return jsonify(all_pre_interview_details)


class VistaInterview(Resource):

    def get(self):
        client = datastore.Client()

        candidate_param = request.args.get('candidate')
        company_param = request.args.get('company')

        # Query all interviews
        interview_query = client.query(kind=interviews_domain)

        if candidate_param:
            candidate_array = [candidate_param]
            interview_query.add_filter('candidates', 'IN', candidate_array)

        if company_param:
            interview_query.add_filter('id_company', '=', company_param)

        interview_results = list(interview_query.fetch())

        all_interview_details = []

        for interview_entity in interview_results:
            # Extract details from the interview entity
            interview_details = {
                'id': interview_entity.key.id,
                'id_company': interview_entity['id_company'],
                'id_offer': interview_entity['id_offer'],
                'candidates': interview_entity['candidates'],
                'link': interview_entity['link'],
                'date': interview_entity['date'],
                'description': interview_entity['description'],
                'result': interview_entity['result'],
            }

            # For each candidate, fetch details from candidates, offers-data, and companies-data entities
            candidate_details = self.get_candidate_details(interview_entity, client)

            interview_details['candidates_details'] = candidate_details
            all_interview_details.append(interview_details)

        return jsonify(all_interview_details)

    def get_candidate_details(self, interview_entity, client):
        # For each candidate, fetch details from candidates, offers-data, and companies-data entities
        candidate_details = []
        for candidate_id in interview_entity['candidates']:
            # Fetch details from candidates entity
            candidate_key = client.key(candidates_domain, int(candidate_id))
            candidate_entity = client.get(candidate_key)

            # Fetch details from offers-data entity
            offer_key = client.key(offers_data_domain, int(interview_entity['id_offer']))
            offer_entity = client.get(offer_key)

            # Fetch details from companies-data entity
            company_key = client.key(companies_data_domain, int(interview_entity['id_company']))
            company_entity = client.get(company_key)

            # Combine all details
            candidate_details.append({
                'candidate': candidate_entity,
                'offer': offer_entity,
                'company': company_entity,
            })
        return candidate_details
