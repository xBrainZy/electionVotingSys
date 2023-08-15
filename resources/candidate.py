import sys
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.candidate import Candidate


class CandidateListResource(Resource):

    def get(self):
        data = Candidate.get_all()

        if data is None:
            return {'message': 'candidate not found'}, HTTPStatus.NOT_FOUND

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        if data['name'] == '' or data['party'] == '':
            return {'message': "candidate's name and party must not be empty"}, HTTPStatus.NOT_FOUND
        
        if len(data['name']) < 3:
            return {'message': 'invalid name, name must be more than 3 characters !'}, HTTPStatus.BAD_REQUEST
        
        if len(data['party']) < 3:
            return {'message': 'invalid party name, it  must be more than 2 characters !'}, HTTPStatus.BAD_REQUEST
        

        candidate = Candidate(name = data['name'],
                        party = data['party']
                        )
        candidate.save()

        return candidate.data, HTTPStatus.CREATED


class CandidateResource(Resource):

    def get(self, candidate_id):
        candidate = Candidate.get_by_id(candidate_id)

        if candidate is None:
            return {'message': 'candidate not found'}, HTTPStatus.NOT_FOUND

        return candidate.data, HTTPStatus.OK

    def put(self, candidate_id):
        data = request.get_json()

        return Candidate.update(candidate_id, data)

    def delete(self, candidate_id):
        return Candidate.un_publish(candidate_id)


class CandidatePublishResource(Resource):

    def put(self, candidate_id):
        return Candidate.publish(candidate_id)

    def delete(self, candidate_id):
        return Candidate.un_publish(candidate_id)
