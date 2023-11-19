from flask_restful import Resource
from flask import request
from flask import jsonify
from google.cloud import datastore
import uuid

from src.utils.utils import get_entity_by_field, update_entity, get_results_from_entity

candidates_domain = 'candidates'
assignments_domain = 'assignments-data'
class VistaPing(Resource):
    def get(self):
        return "Pong"

class VistaCandidatos(Resource): 
    def get(self, id_candidate):

        client = datastore.Client()
        key_candidate = client.key('candidates', int(id_candidate))

        candidate = client.get(key_candidate)

        return {
                'key': candidate.key.path[-1],
                'id_candidato': candidate['id_candidato'],
                'email': candidate['email'],
                'Nombre': candidate['Nombre'],
                'apellido': candidate['apellido'],
                'segundo_nombre': candidate['segundo_nombre'],
                'segundo_apellido': candidate['segundo_apellido'],
                'tipo_documento': candidate['tipo_documento'],
                'documento': candidate['documento'],
                'fecha_nacimiento': candidate['fecha_nacimiento'],
                'genero': candidate['genero'],
                'nacionalidad': candidate['nacionalidad'],
                'estado_civil': candidate['estado_civil'],
                'telefono': candidate['telefono'],
                'pais_nacimiento': candidate['pais_nacimiento'],
                'pais_residencia': candidate['pais_residencia'],
                'ciudad_nacimiento': candidate['ciudad_nacimiento'],
                'ciudad_residencia': candidate['ciudad_residencia'],
                'lenguajes_programacion': candidate['lenguajes_programacion'],
                'tecnologias_herramientas': candidate['tecnologias_herramientas'],
                'educacion': candidate['educacion'],
                'experiencia': candidate['experiencia'],
                'idiomas': candidate['idiomas'],
                'rol':candidate['rol']
            }
        

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
            if entity.get('name') not in unique_names:
                unique_names.add(entity.get('name', ''))
                user_profiles.append({
                    'name': entity.get('name', ''),
                    'type': entity.get('type', ''),
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
        new_profile_id = self.create_user(data)

        return {'message': 'User created successfully', 'profile_id': new_profile_id}, 201

    def create_user(self, data):
        # Initialize the Datastore client
        client = datastore.Client()

        # Create a new Datastore entity for the profile
        key = client.key('candidates')
        candidate = datastore.Entity(key=key)

        # Add attributes to the profile entity
        candidate.update({
            'id_candidato': str(uuid.uuid4()),
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
            'soft_skills': data.get('soft_skill', []),
            'educacion': data.get('educacion', []),
            'experiencia': data.get('experiencia', []),
            'idiomas': data.get('idiomas', []),
            'rol': data.get('rol', [])
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

        # Retrieve optional query parameters
        soft_skills = request.args.getlist('soft_skills')
        rol = request.args.getlist('rol')
        lenguajes_programacion = request.args.getlist('lenguajes_programacion')
        tecnologias_herramientas = request.args.getlist('tecnologias_herramientas')
        idiomas = request.args.getlist('idiomas')

        # Apply filters based on optional query parameters
        if soft_skills:
            query.add_filter('soft_skills', 'in', soft_skills)

        if rol:
            query.add_filter('rol', 'IN', rol)

        if lenguajes_programacion:
            query.add_filter('lenguajes_programacion', 'IN', lenguajes_programacion)

        if idiomas:
            query.add_filter('idiomas.idioma', 'IN', idiomas)

        if tecnologias_herramientas:
            query.add_filter('tecnologias_herramientas', 'IN', tecnologias_herramientas)

        results = query.fetch()

        user_profiles = []

        for entity in results:
            user_profiles.append({
                'key': entity.key.path[-1],
                'id_candidato': entity.get('id_candidato', ''),
                'email': entity.get('email', ''),
                'Nombre': entity.get('Nombre', ''),
                'apellido': entity.get('apellido', ''),
                'segundo_nombre': entity.get('segundo_nombre', ''),
                'segundo_apellido': entity.get('segundo_apellido', ''),
                'tipo_documento': entity.get('tipo_documento', ''),
                'documento': entity.get('documento', ''),
                'fecha_nacimiento': entity.get('fecha_nacimiento', ''),
                'genero': entity.get('genero', ''),
                'nacionalidad': entity.get('nacionalidad', ''),
                'estado_civil': entity.get('estado_civil', ''),
                'telefono': entity.get('telefono', ''),
                'pais_nacimiento': entity.get('pais_nacimiento', ''),
                'pais_residencia': entity.get('pais_residencia', ''),
                'ciudad_nacimiento': entity.get('ciudad_nacimiento', ''),
                'ciudad_residencia': entity.get('ciudad_residencia', ''),
                'lenguajes_programacion': entity.get('lenguajes_programacion', []),
                'tecnologias_herramientas': entity.get('tecnologias_herramientas', []),
                'educacion': entity.get('educacion', []),
                'experiencia': entity.get('experiencia', []),
                'idiomas': entity.get('idiomas', []),
                'rol': entity.get('rol', []),
            })

        return jsonify(user_profiles)


class VistaUserUpdate(Resource):
    def put(self, tab_to_update):
        # Initialize the Datastore client
        client = datastore.Client()
        # Get data from the request
        data = request.get_json()
        id_candidato = data.get('id_candidato', '')
        # Obtener entidad
        candidate = get_entity_by_field(candidates_domain, 'id_candidato', id_candidato)

        # Datos personales
        if 'personal' == tab_to_update:
            update_entity(candidate, {
                'email': data.get('email', ''),
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
                'rol': data.get('rol', []),
                # Add more fields as needed
            })


        # Educación
        if 'education' == tab_to_update:
            update_entity(candidate, {
                'educacion': data.get('educacion', []),
            })
        # Experiencia
        if 'experiencia' == tab_to_update:
            update_entity(candidate, {
                'experiencia': data.get('experiencia', [])
            })
        # Idiomas
        if 'idiomas' == tab_to_update:
            update_entity(candidate, {
                'idiomas': data.get('idiomas', []),
            })

        # Persistir
        client.put(candidate)
        return {'message': 'User updated successfully'}, 200


class VistaCandidatosReady(Resource):
    def get(self):
        required_complete_assignments = ['Technical', 'Performance', 'Language', 'Psychotechnical']
        candidates_ready = []
        # Get Candidates
        candidates = get_results_from_entity(candidates_domain)
        # Get Assignments
        assignments = get_results_from_entity(assignments_domain)
        # Validate completion of all types
        for candidate in candidates:
            candidate_completed_assignments = []
            candidate_id = str(candidate.id)
            for assignment in assignments:
                assignment_candidate = assignment.get('candidate')
                status = assignment.get('status')
                assignment_type = assignment.get('type')
                if assignment_candidate == candidate_id and status == 'finished' and assignment_type \
                        not in candidate_completed_assignments and assignment_type in required_complete_assignments:
                    candidate_completed_assignments.append(assignment_type)
            if len(candidate_completed_assignments) >= 4:
                candidates_ready.append({
                "id": candidate.id,
                "id_candidato": candidate.get('id_candidato'),
                "name": candidate.get('Nombre', '') + ' ' + candidate.get('apellido', '')
            })

        return candidates_ready

