from flask_jwt_extended import create_access_token
from google.cloud import datastore
candidates_entity = 'candidates'
companies_entity = 'companies-data'
users_entity = 'abcjobs-users'

from src.utils.utils import is_correct_password, get_expiration_datetime


def auth_admin_user(email, password):
    # Initialize the Datastore client
    client = datastore.Client()

    # Query all Users
    query = client.query(kind=users_entity).add_filter('email', '=', email)
    results = list(query.fetch())

    try:
        usuario = results.pop()
    except:
        usuario = None
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
    # Initialize the Datastore client
    client = datastore.Client()

    # Query all Candidates
    query = client.query(kind=candidates_entity).add_filter('email', '=', email)
    results = list(query.fetch())

    try:
        candidate = results.pop()
    except:
        candidate = None
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
    # Initialize the Datastore client
    client = datastore.Client()

    # Query all Candidates
    query = client.query(kind=companies_entity).add_filter('email', '=', email)
    results = list(query.fetch())

    try:
        company = results.pop()
    except:
        company = None
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