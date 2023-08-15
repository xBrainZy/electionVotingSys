import sys
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db

from resources.user import UserListResource, UserResource
from resources.voter import VoterListResource, VoterResource, VoterPublishResource
from resources.candidate import CandidateListResource, CandidateResource, CandidatePublishResource
from resources.ballot import BallotListResource, BallotResource, BallotPublishResource, BallotResultResource


def create_app():
    print("Hello", file=sys.stderr)
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<int:user_id>')

    api.add_resource(VoterListResource, '/voters')
    api.add_resource(VoterResource, '/voters/<int:voter_id>')
    api.add_resource(VoterPublishResource, '/voters/<int:voter_id>/publish')

    api.add_resource(CandidateListResource, '/candidates')
    api.add_resource(CandidateResource, '/candidates/<int:candidate_id>')
    api.add_resource(CandidatePublishResource, '/candidates/<int:candidate_id>/publish')
    
    api.add_resource(BallotListResource, '/ballots')
    api.add_resource(BallotResource, '/ballots/<int:ballot_id>')
    api.add_resource(BallotPublishResource, '/ballots/<int:ballot_id>/publish')
    api.add_resource(BallotResultResource, '/ballots/result')
if __name__ == '__main__':
    app = create_app()
    app.run('127.0.0.1', 5000)
