import os
import uuid
from datetime import datetime
from flask_restful import Resource
from flask import request

from src.utils.auth import auth_admin_user, auth_candidate, auth_company
from src.utils.persistence import persist_new_admin_user, persist_new_candidate, persist_new_company
from src.utils.utils import hash_new_password, get_datetime_iso_format




class VistaPing(Resource):
    def get(self):
        return "Pong"


class VistaSignUp(Resource):
    def post(self):
        data = request.get_json()
        # Validate required fields
        required_fields = ['email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return {'message': f'{field} is a required field'}, 400

        role = request.json["role"]
        password = request.json["password"]

        salt, pw_hash = hash_new_password(password)
        today = datetime.now()
        created_date = get_datetime_iso_format(today)
        if role == 'Admin':
            new_user = persist_new_admin_user(data, pw_hash, salt, created_date)
        if role == 'Candidate':
            new_user = persist_new_candidate(data, pw_hash, salt)
        elif role == 'Company':
            new_user = persist_new_company(data, pw_hash, salt, created_date)
        return {
                   "accountCreated": new_user,
                   "createdAt": created_date,
                   "role": data.get('role')
               }, 201


class VistaLogIn(Resource):
    def post(self):
        try:
            email = request.json["email"]
            password = request.json["password"]
            role = request.json["role"]
        except:
            return "", 400
        if email is None or password is None:
            return {"message": "username and password are required fields"}, 400

        if role == 'Admin':
            return auth_admin_user(email, password)
        if role == 'Candidate':
            return auth_candidate(email, password)
        elif role == 'Company':
            return auth_company(email, password)


