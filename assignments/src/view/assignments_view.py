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
assigments_template_entity='assignments-template-data'

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

        key = client.key(assigments_template_entity)
        assignments_ref = datastore.Entity(key=key)

        # Build the assignment data
        assignment_data = {
            'assignment_id': str(uuid.uuid4()),  # Generate a unique ID
            'rol': data['rol'],
            'type': data['type'],
            'focus': data['focus'],
            'questions': data['questions'],
            'status': 'to_do',
            'result': 0.0
        }

        # Store the assignment in Datastore
        assignments_ref.update(assignment_data)
        client.put(assignments_ref)

        return {'message': 'Assignment created successfully', 'assignment_id': assignment_data['assignment_id']}, 201
    

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


    def put(self):
        try:
            # Initialize the Datastore client
            client = datastore.Client()
            data = request.get_json()
            assignment_id = data['assignment_id']

            key = client.key(assigments_entity, int(assignment_id))

            assignment_data = client.get(key)
            questions = assignment_data['questions']
            for question in questions:
                if data['description'] == question['description']:
                    questions.remove(question)
                    break
            if 'resolved_questions' not in assignment_data:
                assignment_data['resolved_questions'] = []

            present_question = False
            for question in assignment_data['resolved_questions']:
                if data['description'] == question['description']:
                    present_question = True
                    break

            if not present_question:
                assignment_data['resolved_questions'].append(data)
            
            if assignment_data['status'] == 'to_do':
                assignment_data['status'] = 'in_progress'
            if len(questions) == 0:
                assignment_data['status'] = 'finished'

            
            key = client.key('assignments-data',int(assignment_id))
            assignments_ref = datastore.Entity(key=key)

            assignment_data['result'] = self.calculate_results(assignment_data['resolved_questions'])
            # Store the assignment in Datastore
            assignments_ref.update(assignment_data)
            client.put(assignments_ref)
            return {'message': 'Assignment updated on question successfully'}, 201

        except Exception as e:
            return {'message': str(e)}, 500
    
    def calculate_results(self,resolved_questions):
        total_questions = len(resolved_questions)
        correct_answers_count = 0

        for question in resolved_questions:
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
        return score_percentage


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
        
        print(f"test finished {assignment_id}")
        return {'message': 'Assignment completed'}, 201

class AssignmentTemplateCandidate(Resource):
    def post(self,assignment_template_id, candidate_key ):
         # Initialize the Datastore client
        client = datastore.Client()
        key = client.key(assigments_template_entity, int(assignment_template_id))
        assignment_data = client.get(key)
        assignment_data['candidate'] = candidate_key

        key_assigment = client.key(assigments_entity)
        assignments_ref = datastore.Entity(key=key_assigment)

        assignments_ref.update(assignment_data)
        client.put(assignments_ref)

        return "Success", 200

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