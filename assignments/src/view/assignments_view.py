import os

from flask_restful import Resource
from flask import request
from flask import jsonify
from google.cloud import datastore
import uuid
from datetime import datetime



class VistaPing(Resource): 
    def get(self):
        return "Pong"


class AssignmentsView(Resource):
    def post(self):
        
        data = request.get_json()

        # Validate required fields
        required_fields = ['rol', 'type', 'focus', 'questions']
        for field in required_fields:
            if field not in data:
                return {'message': f'{field} is a required field'}, 400

        # Initialize the Datastore client
        client = datastore.Client()

        key = client.key('assignments-data')
        assignments_ref = datastore.Entity(key=key)

        # Build the assignment data
        assignment_data = {
            'assignment_id': str(uuid.uuid4()),  # Generate a unique ID
            'rol': data['rol'],
            'type': data['type'],
            'focus': data['focus'],
            'questions': data['questions']
        }

        # Store the assignment in Datastore
        assignments_ref.update(assignment_data)
        client.put(assignments_ref)

        return {'message': 'Assignment created successfully', 'assignment_id': assignment_data['assignment_id']}, 201
    

    def get(self):
    
        # Initialize the Datastore client
        client = datastore.Client()

        # Query all assignments
        query = client.query(kind='assignments-data')
        results = query.fetch()

        assignments = []
        for entity in results:
            assignment_data = {
                'assignment_id': entity.id,
                'rol': entity['rol'],
                'type': entity['type'],
                'focus': entity['focus'],
                'questions': entity['questions']
            }
            assignments.append(assignment_data)

        return jsonify(assignments)

