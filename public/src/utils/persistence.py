import uuid
from google.cloud import datastore

from src.utils.auth import get_entity_by_email

users_entity = 'abcjobs-users'
companies_entity = 'companies-data'
candidates_entity = 'candidates'


def user_exists(entity, email):
    result = get_entity_by_email(entity, email)
    return result is not None


def persist_new_admin_user(data, pw_hash, salt, created_date):
    if user_exists(users_entity, data.get('email')):
        return 0
    new_user = {
        "user_id": str(uuid.uuid4()),
        "username": data.get("username", ""),
        "email": data.get("email"),
        "password_hash": pw_hash,
        "salt": salt,
        "role": data.get("role"),
        "created_date": created_date,
        "last_modified": created_date,
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "document_type": data.get("document_type", ""),
        "document_number": data.get("document_number", ""),
        "birth_date": data.get("birth_date", ""),
        "gender": data.get("gender", ""),
        "country": data.get("country", ""),
        "marital_status": data.get("marital_status", ""),
        "city": data.get("city", ""),
        "department": data.get("department", ""),
        "nationality": data.get("nationality", ""),
    }
    # Initialize the Datastore client
    client = datastore.Client()

    key = client.key(users_entity)
    users_ref = datastore.Entity(key=key)
    users_ref.update(new_user)
    client.put(users_ref)
    return str(users_ref.id)


def persist_new_company(data, pw_hash, salt, created_date):
    if user_exists(companies_entity, data.get('email')):
        return 0
    new_company = {
        "company_id": str(uuid.uuid4()),
        "password_hash": pw_hash,
        "salt": salt,
        "document_type": data.get("document_type", ""),
        "document_number": data.get("document_number", ""),
        "name": data.get("name", ""),
        "phone_number": data.get("phone_number", ""),
        "country": data.get("country", ""),
        "email": data.get("email", ""),
        "created_date": created_date,
        "last_modified": created_date,
    }
    # Initialize the Datastore client
    client = datastore.Client()

    key = client.key(companies_entity)
    companies_ref = datastore.Entity(key=key)
    companies_ref.update(new_company)
    client.put(companies_ref)
    return str(companies_ref.id)


def persist_new_candidate(data, pw_hash, salt):
    if user_exists(candidates_entity, data.get('email')):
        return 0
    new_candidate = {
        'id_candidato': str(uuid.uuid4()),
        "password_hash": pw_hash,
        "salt": salt,
        "email": data.get("email", ""),
        "Nombre": data.get("Nombre", ""),
        "apellido": data.get("apellido", ""),
        "segundo_nombre": data.get("segundo_nombre", ""),
        "segundo_apellido": data.get("segundo_apellido", ""),
        "tipo_documento": data.get("documento", ""),
        "documento": data.get("documento", ""),
        "fecha_nacimiento": data.get("fecha_nacimiento", ""),
        "genero": data.get("genero", ""),
        "nacionalidad": data.get("nacionalidad", ""),
        "estado_civil": data.get("estado_civil", ""),
        "telefono": data.get("telefono", ""),
        "pais_nacimiento": data.get("pais_nacimiento", ""),
        "pais_residencia": data.get("pais_residencia", ""),
        "ciudad_nacimiento": data.get("ciudad_nacimiento", ""),
        "rol": data.get("rol", []),
        "lenguajes_programacion": data.get("lenguajes_programacion", []),
        "tecnologias_herramientas": data.get("tecnologias_herramientas", []),
        "soft_skill": data.get("soft_skill", []),
        "ciudad_residencia": data.get("ciudad_residencia", ""),
        "educacion": data.get("educacion", []),
        "experiencia": data.get("experiencia", []),
        "idiomas": data.get("idiomas", [])
    }
    # Initialize the Datastore client
    client = datastore.Client()

    # Create a new Datastore entity for the profile
    key = client.key(candidates_entity)
    candidate = datastore.Entity(key=key)
    candidate.update(new_candidate)
    client.put(candidate)
    return str(candidate.id)
