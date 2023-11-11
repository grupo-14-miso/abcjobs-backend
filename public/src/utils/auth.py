from flask_jwt_extended import create_access_token
from google.cloud import datastore

candidates_entity = 'candidates'
companies_entity = 'companies-data'
users_entity = 'abcjobs-users'

from src.utils.utils import is_correct_password, get_expiration_datetime


def get_entity_by_email(entity, email):
    # Initialize the Datastore client
    client = datastore.Client()

    # Query all Users
    query = client.query(kind=entity).add_filter('email', '=', email)
    results = list(query.fetch())
    try:
        return results.pop()
    except:
        return None


def auth_admin_user(email, password):
    usuario = get_entity_by_email(users_entity, email)
    if usuario is not None:
        salt = usuario.get('salt')
        pw_hash = usuario.get('password_hash')
        user_id = usuario.get('user_id')
        if is_correct_password(salt, pw_hash, password):
            token = create_access_token(identity=user_id)
            expiration_date = get_expiration_datetime()
            return {"id": user_id,
                    "token": token,
                    "expireAt": expiration_date,
                    "role": usuario.get('role'),
                    "name": usuario.get('first_name') + " " + usuario.get('last_name')}, 200
        else:
            return "Usuario o contraseña incorrectos", 422
    else:
        return "", 404


def auth_candidate(email, password):
    candidate = get_entity_by_email(candidates_entity, email)

    if candidate is not None:
        salt = candidate.get('salt')
        pw_hash = candidate.get('password_hash')
        id_candidato = candidate.get('id_candidato')
        if is_correct_password(salt, pw_hash, password):
            token = create_access_token(identity=id_candidato)
            expiration_date = get_expiration_datetime()
            return {"id": id_candidato,
                    "token": token,
                    "expireAt": expiration_date,
                    "role": 'Candidate',
                    "name": candidate.get('Nombre') + " " + candidate.get('apellido')}, 200
        else:
            return "Email o contraseña incorrectos", 422
    else:
        return "", 404


def auth_company(email, password):
    company = get_entity_by_email(companies_entity, email)
    if company is not None:
        salt = company.get('salt')
        pw_hash = company.get('password_hash')
        company_id = company.get('company_id')
        if is_correct_password(salt, pw_hash, password):
            token = create_access_token(identity=company_id)
            expiration_date = get_expiration_datetime()
            return {"id": company_id,
                    "token": token,
                    "expireAt": expiration_date,
                    "role": 'Company',
                    "name": company.get('name')}, 200
        else:
            return "Email o contraseña incorrectos", 422
    else:
        return "", 404
