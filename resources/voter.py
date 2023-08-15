import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.voter import Voter

from models.voter import Validate




class VoterListResource(Resource):

    def get(self):
        data = Voter.get_all()

        if data is None:
            return {'message': 'voter not found'}, HTTPStatus.NOT_FOUND

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        if data['name'] == '' or data['address'] == '' or data['DOB'] == '':
            return {'message': "voter's name, address and the date of birth must not be empty"}, HTTPStatus.NOT_FOUND
        
        if len(data['name']) < 3:
            return {'message': 'invalid name, name must be more than 3 characters !'}, HTTPStatus.BAD_REQUEST
        
        if ((len(data['address']) < 3) or (',' not in data['address']) ):
            return {'message': 'invalid location, name must be more than 3 characters !'}, HTTPStatus.BAD_REQUEST
        
        
        if not Validate.ageCalculator(data['DOB']):
            return {'message': "Voter's age must be 18 or older to be eligible to vote"}
        
        voter = Voter(name = data['name'],
                        address = data['address'],
                        dob = Validate.dateCaster(data['DOB']),
                        user_id=data["user_id"]
                        )
        voter.save()

        return voter.data, HTTPStatus.CREATED


class VoterResource(Resource):

    def get(self, voter_id):
        voter = Voter.get_by_id(voter_id)

        if voter is None:
            return {'message': 'voter not found'}, HTTPStatus.NOT_FOUND

        return voter.data, HTTPStatus.OK

    def put(self, voter_id):
        data = request.get_json()

        return Voter.update(voter_id, data)

    
    def delete(self, voter_id):
        return Voter.un_publish(voter_id)


class VoterPublishResource(Resource):

    def put(self, voter_id):
        return Voter.publish(voter_id)

    def delete(self, voter_id):
        return Voter.un_publish(voter_id)
