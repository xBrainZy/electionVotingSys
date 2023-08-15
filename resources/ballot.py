import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.ballot import Ballot


class BallotListResource(Resource):

    def get(self):
        data = Ballot.get_all()

        if data is None:
            return {'message': 'ballot not found'}, HTTPStatus.NOT_FOUND

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        if data['voter_id'] == '' or data['candidate_id'] == '':
            return {'message': "voter's id and candidate's id must not be empty"}, HTTPStatus.NOT_FOUND
        
        
        
        ballot = Ballot(voter_id = data['voter_id'],
                        candidate_id = data['candidate_id'])
        ballot.save()

        return ballot.data, HTTPStatus.CREATED


class BallotResource(Resource):

    def get(self, ballot_id):
        ballot = Ballot.get_by_id(ballot_id)

        if ballot is None:
            return {'message': 'ballot not found'}, HTTPStatus.NOT_FOUND

        return ballot.data, HTTPStatus.OK

    def put(self, ballot_id):
        data = request.get_json()

        return Ballot.update(ballot_id, data)

    def delete(self, ballot_id):
        return Ballot.un_publish(ballot_id)


class BallotPublishResource(Resource):

    def put(self, ballot_id):
        return Ballot.publish(ballot_id)

    def delete(self, ballot_id):
        return Ballot.un_publish(ballot_id)
    
class BallotResultResource(Resource):

    def get(self):
        return Ballot.finalResult() 
