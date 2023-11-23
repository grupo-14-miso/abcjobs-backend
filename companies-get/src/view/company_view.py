from flask import jsonify
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



