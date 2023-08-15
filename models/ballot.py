import sys
from extensions import db
from resources.voter import VoterListResource
from models.voter import Voter
from resources.candidate import CandidateListResource
from models.candidate import Candidate
from http import HTTPStatus


class Ballot(db.Model):
    __tablename__ = 'ballot'

    id = db.Column(db.Integer, primary_key=True)
    is_publish = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    voter_id = db.Column(db.Integer(), db.ForeignKey("voter.id"), unique=True, nullable=False)
    candidate_id = db.Column(db.Integer(), db.ForeignKey("candidate.id"), unique=False, nullable=False)

    

    @property
    def data(self):
        return {
            'id': self.id,
            'voter_name': Voter.get_name_by_id(self.voter_id),
            'candidate_name': Candidate.get_name_by_id(self.candidate_id)
        }
    @property
    def get_candidate_id(self):
        return self.candidate_id

    

    @classmethod
    def get_all(cls):
        r = cls.query.filter_by(is_publish=True).all()

        result = []

        for i in r:
            result.append(i.data)

        return result

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter((cls.id == id) & (cls.is_publish == True)).first()
    
    
        
    
    @classmethod
    def get_by_id_n(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_publish == False)).first()
        return x

    @classmethod
    def update(cls, id, data):
        ballot = cls.query.filter(cls.id == id).first()

        if ballot is None:
            return {'message': 'ballot not found'}, HTTPStatus.NOT_FOUND
        
        if not Candidate.get_by_id_bool(data['candidate_id']):
            return {'message': " enter correct candidate's id"}, HTTPStatus.NOT_FOUND

         
        ballot.candidate_id = data['candidate_id']
        
        
        db.session.commit()
        return ballot.data, HTTPStatus.OK

    @classmethod
    def delete(cls, id):
        ballot = cls.query.filter(cls.id == id).first()
        if ballot is None:
            return {'message': 'ballot not found'}, HTTPStatus.NOT_FOUND

        db.session.delete(ballot)
        db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    @classmethod
    def publish(cls, ballot_id):
        ballot = Ballot.get_by_id_n(ballot_id)
        if ballot is None:
            return {'message': 'ballot not found'}, HTTPStatus.NOT_FOUND

        ballot.is_publish = True
        db.session.commit()
        return ballot.data, HTTPStatus.OK

    @classmethod
    def un_publish(cls, ballot_id):
        ballot = Ballot.get_by_id(ballot_id)
        if ballot is None:
            return {'message': 'ballot not found'}, HTTPStatus.NOT_FOUND

        ballot.is_publish = False
        db.session.commit()
        return ballot.data, HTTPStatus.OK
    
    @classmethod
    def voteCount(cls, id):
        candidateVoteCount = cls.query.filter(cls.candidate_id == id).count()
        if candidateVoteCount is None:
            return {'message': 'votes not found'}, HTTPStatus.NOT_FOUND
        
        return candidateVoteCount
        

    @classmethod
    def voteResultGenerator(cls):
        allCandidatesInBallot =  cls.query.filter_by(is_publish=True).all() # [ list of objects]
        
        #totalVotes = len(allCandidatesInBallot)

        res = {}

        for item in allCandidatesInBallot:
            x = res.get(item.get_candidate_id)
            if x is None:
                res[Candidate.get_name_by_id(item.get_candidate_id)] = cls.voteCount(item.get_candidate_id)
            
        return res 
    
    @classmethod
    def finalResult(cls):
        res = cls.voteResultGenerator()

        votingPercentages = list(res.values())

        mostVotes = max(votingPercentages)
        indexMax = votingPercentages.index(mostVotes)

        candidateName = list(res.keys())[indexMax]

        return {candidateName: f'{candidateName} is the winner !! with {mostVotes} votes'}, HTTPStatus.OK
            
        
    
    def save(self):
        db.session.add(self)
        db.session.commit()
