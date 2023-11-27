from flask_restful import Resource
from flask import request
from flask import jsonify
from google.cloud import datastore

from src.utils.utils import get_results_from_entity, get_entities_by_field, get_candidates_ready

candidates_domain = 'candidates'
assignments_domain = 'assignments-data'
pre_interview_domain = 'pre_interview'
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
                'soft_skill': candidate.get('soft_skills', []),
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


class VistaUsers(Resource):
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
            query.add_filter('soft_skills', 'IN', soft_skills)

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
                'soft_skill': entity.get('soft_skills', []),
                'educacion': entity.get('educacion', []),
                'experiencia': entity.get('experiencia', []),
                'idiomas': entity.get('idiomas', []),
                'rol': entity.get('rol', []),
            })

        return jsonify(user_profiles)



class VistaCandidatosReady(Resource):
    def get(self, id_offer):
        required_complete_assignments = ['Technical', 'Language', 'Psychotechnical']
        # Get Pre Interviews By Offer
        pre_interwiews = get_entities_by_field(pre_interview_domain, 'id_offer', id_offer)
        candidates_on_pre_interview = []
        for pre_interwiew in pre_interwiews:
            candidates_on_pre_interview.append(pre_interwiew.get('id_candidate'))

        # Get Candidates
        candidates = get_results_from_entity(candidates_domain)
        # Get Assignments
        assignments = get_results_from_entity(assignments_domain)
        # Validate completion of all types
        candidates_ready = get_candidates_ready(candidates, assignments, candidates_on_pre_interview, required_complete_assignments)

        return candidates_ready

