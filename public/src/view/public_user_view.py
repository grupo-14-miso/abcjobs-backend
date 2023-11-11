import os
import uuid
from datetime import datetime
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from flask import request
from google.cloud import datastore
import requests

from src.utils.utils import is_correct_password, get_expiration_datetime, hash_new_password, get_datetime_iso_format

candidates_entity = 'candidates'
companies_entity = 'companies-data'
users_entity = 'abcjobs-users'

class VistaPing(Resource): 
    def get(self):
        return "Pong"

class VistaSignUp(Resource):
    def post(self):
        try:
            username = request.json["username"]
            email = request.json["email"]
            password = request.json["password"]
            role = request.json["role"]
            data = request.get_json()
        except:
            return "", 400
        if username is None or email is None or password is None:
            return "", 400

        salt, pw_hash = hash_new_password(password)
        today = datetime.now()
        created_date = get_datetime_iso_format(today)
        new_user = {
                "user_id": str(uuid.uuid4()),
                "username": username,
                "email": email,
                "password_hash": pw_hash,
                "salt": salt,
                "role": role,
                "created_date": created_date,
                "last_modified": created_date,
                "first_name": "Robert",
                "last_name": "Lewandowski",
                "document_type": "CC",
                "document_number": "32254324",
                "birth_date": "1956-10-30",
                "gender": "H",
                "country": "Poland",
                "marital_status": "C",
                "city": "Barcelona",
                "department": "Cataluña",
                "nationality": "Polish",
            }
        # Initialize the Datastore client
        client = datastore.Client()

        key = client.key(users_entity)
        users_ref = datastore.Entity(key=key)
        users_ref.update(new_user)
        client.put(users_ref)
        return {
            "id": new_user.get('user_id'),
            "createdAt": created_date
               }, 201


class VistaLogIn(Resource):
    def post(self):
        try:
            username = request.json["username"]
            password = request.json["password"]
        except:
            return "", 400
        if username is None or password is None:
            return {"message": "username and password are required fields"}, 400

        # Initialize the Datastore client
        client = datastore.Client()

        # Query all assignments
        query = client.query(kind=users_entity).add_filter('username', '=', username)
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