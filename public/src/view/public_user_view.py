from datetime import datetime
from flask_restful import Resource
from flask import request, jsonify


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
        new_user = None
        if role == 'Admin':
            new_user = persist_new_admin_user(data, pw_hash, salt, created_date)
        if role == 'Candidate':
            new_user = persist_new_candidate(data, pw_hash, salt)
        if role == 'Company':
            new_user = persist_new_company(data, pw_hash, salt, created_date)
        if new_user == 0:
            return {'message': role + ' already exists'}, 400
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

class VistaValidate(Resource):
    def post(self):
        token = request.headers.get('Authorization')
        path = request.path
        
        print("Request Method:", request.method)
        print("Request Path:", request.path)
        print("Request Full Path:", request.full_path)
        print("Request URI:", request.url)
        print("Request Headers:", request.headers)
        print("Request JSON Data:", request.json if request.is_json else None)
        print("Request Form Data:", request.form if request.form else None)



        if "/public/register" in path or "/public/login" in path:
            return {"status": "ok", "message": "Special path accessed."}, 200
        elif token and self.validate_token_function(token):
            return {"status": "success", "message": "Token is valid. Access granted."}, 200
        else:
            return {"status": "error", "message": "Token is invalid or expired. Access denied."}, 401

    def validate_token_function(self,token):
        # Placeholder for token validation logic
        # Implement your actual token validation logic here
        # For example, check if the token is a valid JWT
        print(token)
        return True

