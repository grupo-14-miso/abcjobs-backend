import os

from flask_restful import Resource
from flask import request
from flask import jsonify
from google.cloud import datastore
import uuid
from datetime import datetime
from google.cloud import pubsub_v1
import json



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
                'questions': entity['questions'],
                'status': entity['status'],
                'result': entity['result']
            }
            assignments.append(assignment_data)

        return jsonify(assignments)

class AssignmentSubmissionView(Resource):
    def __init__(self, publisher, topic_path):
        self.publisher = publisher
        self.topic_path = topic_path

    def post(self, assignment_id):
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = ['answers', 'correct_answer', 'selected_answer', 'description']
            for field in required_fields:
                if field not in data:
                    return {'message': f'{field} is a required field'}, 400

            # Add created_timestamp to the message
            data['created_timestamp'] = datetime.utcnow().isoformat()

            # Publish the message to Pub/Sub
            message = {
                'assignment_id': assignment_id,
                'answers': data['answers'],
                'correct_answer': data['correct_answer'],
                'selected_answer': data['selected_answer'],
                'description': data['description'],
                'created_timestamp': data['created_timestamp']
            }

            message_data = json.dumps(message).encode('utf-8')
            future = self.publisher.publish(self.topic_path, data=message_data)
            future.result()  # Wait for the message to be published

            return {'message': 'Assignment submitted successfully'}, 201

        except Exception as e:
            return {'message': str(e)}, 500