from flask import request
from flask_restful import Resource
from http import HTTPStatus

from utils import hash_password
from models.user import User

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        # Do not add the user if the username is taken
        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        # Do not add the user if the email is taken
        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        if len(username) < 2:
            return {'message': 'invalid username, username must be more than 2 characters !'}, HTTPStatus.BAD_REQUEST
        
        if '@' not in email:
            return {'message': 'invalid email'}, HTTPStatus.BAD_REQUEST


        password = hash_password(non_hash_password)

        user = User(
            username=username,
            email=email,
            password=password
        )

        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return data, HTTPStatus.CREATED
    
    def get(self):

        data = User.get_all()

        if data is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        return {'data': data}, HTTPStatus.OK
    

class UserResource(Resource):

    def get(self, user_id):
        user = User.get_by_id(user_id)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        return user.data, HTTPStatus.OK


    def put(self, user_id):
        data = request.get_json()

        return User.update(user_id, data)
    
    def delete(self, user_id):
        
        return User.un_publish(user_id)
