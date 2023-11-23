import os

from flask_restful import Resource
from flask import request
from flask import jsonify
from google.cloud import datastore
import uuid
from datetime import datetime
import json

assigments_entity='assignments-data'
assigments_template_entity='assignments-template-data'

class VistaPing(Resource): 
    def get(self):
        return "Pong"


class AssignmentsView(Resource):

    def get(self):
    
        # Initialize the Datastore client
        client = datastore.Client()

        # Query all assignments
        query = client.query(kind=assigments_template_entity)
        
        status = request.args.getlist('status')

        type = request.args.getlist('type')

        if status:
            query.add_filter('status', 'IN', status)
        
        if type:
            query.add_filter('type', 'IN', type)
        
        results = query.fetch()
        
        

        assignments = []
        for entity in results:
            assignment_data = {
                'assignment_id': entity.id,
                'rol': entity['rol'],
                'type': entity['type'],
                'focus': entity['focus'],
                'questions': entity['questions'],
                'status': entity['status'],
                'result': entity['result']
            }
            assignments.append(assignment_data)

        return jsonify(assignments)


class AssignmentTemplateCandidate(Resource):

    def get(sefl, candidate_key):
        # Initialize the Datastore client
        client = datastore.Client()
        query = client.query(kind=assigments_entity)
        query.add_filter('candidate', '=', candidate_key)
        results = query.fetch()
        
        status = request.args.getlist('status')


        if status:
            query.add_filter('status', 'IN', status)
        

        assignments = []
        for entity in results:
            assignment_data = {
                'assignment_id': entity.id,
                'rol': entity['rol'],
                'type': entity['type'],
                'focus': entity['focus'],
                'questions': entity['questions'],
                'status': entity['status'],
                'result': entity['result']
            }
            assignments.append(assignment_data)

        return jsonify(assignments)

class AssignmentPerformanceCompany(Resource):

    def get(self, id_company):
        client = datastore.Client()
        pre_interview_query = client.query(kind='pre_interview')
        pre_interview_query.add_filter('id_company', '=', id_company)
        pre_interview_entities = list(pre_interview_query.fetch())
        
        assignments_to_return = []

        for pre_interview_entity in pre_interview_entities:
            id_candidate = pre_interview_entity['id_candidate']

            assigment_query = client.query(kind='assignments-data')
            assigment_query.add_filter('candidate', '=', id_candidate)
            assigment_query.add_filter('type', '=', 'Performance')

            assignments = list(assigment_query.fetch())
            for assignment in assignments :
                key_candidate = client.key('candidates', int(id_candidate))
                candidate = client.get(key_candidate)
                if candidate:
                    assignment_data = {
                    'assignment_id': assignment.key.id,
                    'rol': assignment['rol'],
                    'type': assignment['type'],
                    'focus': assignment['focus'],
                    'questions': assignment['questions'],
                    'status': assignment['status'],
                    'result': assignment['result'],
                    'nombre': candidate['Nombre'],
                    'apellido': candidate['apellido']
                    }
                assignments_to_return.append(assignment_data)

        return jsonify(assignments_to_return)