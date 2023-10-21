import os

from flask_restful import Resource
from flask import request
from flask import jsonify
from google.cloud import datastore
import uuid
from datetime import datetime
from google.cloud import pubsub_v1
import json

assigments_entity='assignments-data'

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

        key = client.key(assigments_entity)
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
        query = client.query(kind=assigments_entity)
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

class QuestionnaireView(Resource):
    def post(self, assignment_id) :
        client = datastore.Client()
        key = client.key(assigments_entity, int(assignment_id))

        # Use the key to retrieve the entity
        entity = client.get(key)
        if entity:
            entity['status'] = 'finished'

            entity['status'] = 'finished'

            # Calculate the score based on resolved_questions
            total_questions = len(entity['resolved_questions'])
            correct_answers_count = 0

            for question in entity['resolved_questions']:
                correct_answers = question.get('correct_answer', [])
                selected_answers = question.get('selected_answer', [])

                # Check if at least one selected answer matches any correct answer
                if any(answer in correct_answers for answer in selected_answers):
                    correct_answers_count += 1

            # Calculate the percentage of correct answers
            if total_questions > 0:
                score_percentage = (correct_answers_count / total_questions) * 100
            else:
                score_percentage = 0

            # Update the 'score' attribute
            entity['result'] = score_percentage

            # Save the changes back to Firestore
            client.put(entity)
        else:
            print(f"No record found with key {assignment_id}")
        return {'message': 'Assignment completed'}, 201
