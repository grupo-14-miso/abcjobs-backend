import os

from flask_restful import Resource
from flask import request
import requests
from flask import jsonify
from google.cloud import datastore


class VistaPing(Resource): 
    def get(self):
        return "Pong"

class VistaUserProfile(Resource):
    def get(self):
       
        # Initialize the Datastore client
        client = datastore.Client()
        # Query all user profiles
        query = client.query(kind='profiles')
        results = query.fetch()
        # Create a set to store unique names
        unique_names = set()
        user_profiles = []
        for entity in results:
            # Check if the name is unique
            if entity['name'] not in unique_names:
                unique_names.add(entity['name'])
                user_profiles.append({
                    'name': entity['name'],
                    'type': entity['type'],
                    # Add more fields as needed
                })

         # Create a dictionary to store profiles grouped by type
        profiles_by_type = {}
        for entity in user_profiles:
            profile_type = entity['type']
            # If the type is not already a key in the dictionary, create an empty list
            if profile_type not in profiles_by_type:
                profiles_by_type[profile_type] = []
            # Append the profile details to the list for the corresponding type
            profiles_by_type[profile_type].append({
                'name': entity['name'],
                'type': entity['type'],
                # Add more fields as needed
            })
        # Convert the dictionary values to a list before returning
        user_profiles_grouped_by_type = list(profiles_by_type.values())
        return jsonify(user_profiles_grouped_by_type)


    def post(self):
        # Get data from the request
        data = request.get_json()

        # Validate required fields
        if 'name' not in data or 'type' not in data:
            return {'message': 'Name and type are required fields'}, 400

        # Add the new profile to the Firebase database
        new_profile_id = self.create_profile(data['name'], data['type'])

        return {'message': 'Profile created successfully', 'profile_id': new_profile_id}, 201

    def create_profile(self, name, profile_type):
        # Initialize the Datastore client
        client = datastore.Client()

        # Create a new Datastore entity for the profile
        key = client.key('profiles')
        new_profile = datastore.Entity(key=key)
        new_profile.update({
            'name': name,
            'type': profile_type,
            # Add more fields as needed
        })

        # Save the entity to Datastore
        client.put(new_profile)
        

        return str(key.id)
