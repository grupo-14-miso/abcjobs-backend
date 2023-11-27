import uuid
from datetime import date

from flask import request, jsonify
from flask_restful import Resource
from google.cloud import datastore

from src.utils.utils import get_entities_by_field

companies_entity = 'companies-data'
offers_entity = 'offers-data'
equipos_entity = 'equipos-data'

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

    def get(self):
        # Initialize the Datastore client
        client = datastore.Client()

        # Query all assignments
        query = client.query(kind=companies_entity)

        results = query.fetch()

        companies = []
        for data in results:
            company_data = {
                'company_id': data.id,
                'document_type': data['document_type'],
                'document_number': data['document_number'],
                'name': data['name'],
                'phone_number': data['phone_number'],
                'country': data['country'],
                'email': data['email'],
                'created_date': data['created_date'],
                'last_modified': data['last_modified']
            }
            companies.append(company_data)
        return jsonify(companies)


class OfferByIdView(Resource):
    def get(self, offer_id):
        client = datastore.Client()
        key_offer = client.key(offers_entity, int(offer_id))
        offer = client.get(key_offer)
        return {
                'offer_id': offer.id,  # Generate a unique ID
                'company_id': offer.get('company_id'),
                'name': offer.get('name'),
                'description': offer.get('description'),
                'start_date': offer.get('start_date'),
                'end_date': offer.get('end_date'),
                'created_date': offer.get('created_date'),
                'last_modified': offer.get('last_modified')
            }


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

class OfferByCompanyView(Resource):
    def get(self, company_id):
        # Initialize the Datastore client
        client = datastore.Client()

        # Query all assignments
        query = client.query(kind=offers_entity).add_filter('company_id', '=', company_id)

        results = query.fetch()

        offers = []

        for data in results:
            offer_data = {
                'offer_id': data.id,  # Generate a unique ID
                'company_id': data['company_id'],
                'name': data['name'],
                'description': data['description'],
                'start_date': data['start_date'],
                'end_date': data['end_date'],
                'created_date': data['created_date'],
                'last_modified': data['last_modified']
            }
            offers.append(offer_data)
        return jsonify(offers)


class EquipoView(Resource):
    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = ['offer_id', 'candidate_id']
        for field in required_fields:
            if field not in data:
                return {'message': f'{field} is a required field'}, 400

        # Initialize the Datastore client
        client = datastore.Client()

        key = client.key(equipos_entity)
        equipos_ref = datastore.Entity(key=key)

        #Build equipo entity
        equipos_data = {
            "offer_id": data.get('offer_id'),
            "candidate_id": data.get('candidate_id'),
            "nombre": data.get('nombre', ''),
            "tipo": data.get('tipo', 'interno'),
            "rol": data.get('rol', ''),
            "estado": 'Activo'
        }

        equipos_ref.update(equipos_data)
        client.put(equipos_ref)
        return {'message': 'Candidate added successfully', 'offer_id': data['offer_id']}, 201


class EquipoByOfferView(Resource):
    def get(self, offer_id):
        miembros_equipo = get_entities_by_field(equipos_entity, 'offer_id', offer_id)
        members = []
        for data in miembros_equipo:
            equipo_data = {
                'offer_id': data.get('offer_id'),
                'candidate_id': data.get('candidate_id'),
                'tipo': data.get('tipo'),
                'rol': data.get('rol'),
                'nombre': data.get('nombre'),
                'estado': data.get('estado')
            }
            members.append(equipo_data)
        return jsonify(members)



