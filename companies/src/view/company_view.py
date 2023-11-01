import uuid
from datetime import date

from flask import request
from flask_restful import Resource
from google.cloud import datastore

companies_entity = 'companies-data'
offers_entity = 'offers-data'

class VistaPing(Resource): 
    def get(self):
        return "Pong"


class CompanyView(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = []
        for field in required_fields:
            if field not in data:
                return {'message': f'{field} is a required field'}, 400

        # Initialize the Datastore client
        client = datastore.Client()

        key = client.key(companies_entity)
        companies_ref = datastore.Entity(key=key)

        #Build the company data
        company_data = {
            'company_id': str(uuid.uuid4()),  # Generate a unique ID
            'document_type': data['document_type'],
            'document_number': data['document_number'],
            'name': data['name'],
            'phone_number': data['phone_number'],
            'country': data['country'],
            'email': data['email'],
            'created_date': date.today().strftime("%Y-%m-%d"),
            'last_modified': date.today().strftime("%Y-%m-%d")
        }

        companies_ref.update(company_data)
        client.put(companies_ref)
        return {'message': 'Company created successfully', 'company_id': company_data['company_id']}, 201

class OfferView(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = []
        for field in required_fields:
            if field not in data:
                return {'message': f'{field} is a required field'}, 400

        # Initialize the Datastore client
        client = datastore.Client()

        key = client.key(offers_entity)
        offers_ref = datastore.Entity(key=key)

        # Build the company data
        offers_data = {
            'offer_id': str(uuid.uuid4()),  # Generate a unique ID
            'company_id': data['company_id'],
            'name': data['name'],
            'description': data['description'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'created_date': date.today().strftime("%Y-%m-%d"),
            'last_modified': date.today().strftime("%Y-%m-%d")
        }

        offers_ref.update(offers_data)
        client.put(offers_ref)
        return {'message': 'Offer created successfully', 'offer_id': offers_data['offer_id']}, 201

