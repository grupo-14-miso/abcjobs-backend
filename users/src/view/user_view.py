import os

from flask_restful import Resource
from flask import request
import requests
from flask import jsonify
from google.cloud import datastore
import uuid



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

        profiles_by_type = {}
        for profile in user_profiles:
            profile_type = profile['type']
            if profile_type not in profiles_by_type:
                profiles_by_type[profile_type] = []
            profiles_by_type[profile_type].append(profile)

        # Convert the dictionary values to a list before returning
        grouped_profiles = [{'type': profile_type, 'names': [entry['name'] for entry in entries]}
                            for profile_type, entries in profiles_by_type.items()]

        return jsonify(grouped_profiles)
    



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


class VistaUsers(Resource):
    def post(self):
        # Get data from the request
        data = request.get_json()


        # Add the new profile to the Firebase database
        new_profile_id = self.create_profile(data)

        return {'message': 'Profile created successfully', 'profile_id': new_profile_id}, 201

    def create_profile(self, data):
        # Initialize the Datastore client
        client = datastore.Client()

        # Create a new Datastore entity for the profile
        key = client.key('candidates')
        candidate = datastore.Entity(key=key)
        
        # Add attributes to the profile entity
        candidate.update({
            'id_candidato': str(uuid.uuid4()),
            'email': data.get('email', ''),
            'email': data.get('email', ''),
            'password': data.get('password', ''),
            'Nombre': data.get('Nombre', ''),
            'apellido': data.get('apellido', ''),
            'segundo_nombre': data.get('segundo_nombre', ''),
            'segundo_apellido': data.get('segundo_apellido', ''),
            'tipo_documento': data.get('tipo_documento', ''),
            'documento': data.get('documento', ''),
            'fecha_nacimiento': data.get('fecha_nacimiento', ''),
            'genero': data.get('genero', ''),
            'nacionalidad': data.get('nacionalidad', ''),
            'estado_civil': data.get('estado_civil', ''),
            'telefono': data.get('telefono', ''),
            'pais_nacimiento': data.get('pais_nacimiento', ''),
            'pais_residencia': data.get('pais_residencia', ''),
            'ciudad_nacimiento': data.get('ciudad_nacimiento', ''),
            'ciudad_residencia': data.get('ciudad_residencia', ''),
            'lenguajes_programacion': data.get('lenguajes_programacion', []),
            'tecnologias_herramientas': data.get('tecnologias_herramientas', []),
            'soft_skills': data.get('tecnologias_herramientas', []),
            'educacion': data.get('educacion', []),
            'experiencia': data.get('experiencia', []),
            'idiomas': data.get('idiomas', [])
        })

        # Save the entity to Datastore
        client.put(candidate)

        return str(key.id)
    
    def get(self):
        # Initialize the Datastore client
        client = datastore.Client()

        # Query all user profiles
        query = client.query(kind='candidates')
        results = query.fetch()

        user_profiles = []
        for entity in results:
            user_profiles.append({
                'id_candidato': entity['id_candidato'],
                'email': entity['email'],
                'password': entity['password'],
                'Nombre': entity['Nombre'],
                'apellido': entity['apellido'],
                'segundo_nombre': entity['segundo_nombre'],
                'segundo_apellido': entity['segundo_apellido'],
                'tipo_documento': entity['tipo_documento'],
                'documento': entity['documento'],
                'fecha_nacimiento': entity['fecha_nacimiento'],
                'genero': entity['genero'],
                'nacionalidad': entity['nacionalidad'],
                'estado_civil': entity['estado_civil'],
                'telefono': entity['telefono'],
                'pais_nacimiento': entity['pais_nacimiento'],
                'pais_residencia': entity['pais_residencia'],
                'ciudad_nacimiento': entity['ciudad_nacimiento'],
                'ciudad_residencia': entity['ciudad_residencia'],
                'lenguajes_programacion': entity['lenguajes_programacion'],
                'tecnologias_herramientas': entity['tecnologias_herramientas'],
                'educacion': entity['educacion'],
                'experiencia': entity['experiencia'],
                'idiomas': entity['idiomas'],
            })

        return jsonify(user_profiles)