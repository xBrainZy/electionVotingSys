import sys
from extensions import db
from http import HTTPStatus


class Candidate(db.Model):
    __tablename__ = 'candidate'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(200), nullable=False)
    
    
    is_publish = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    ballots = db.relationship('Ballot', backref='candidate')
    

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'party': self.party
        }

    

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
    def get_by_id_bool(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_publish == True)).first()

        if not x:
            return False

        return True
    
    @classmethod
    def get_by_id_n(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_publish == False)).first()
        return x

    @classmethod
    def get_name_by_id(cls, candidate_id):
        return cls.query.filter_by(id=candidate_id).first().name
    
    @classmethod
    def update(cls, id, data):
        candidate = cls.query.filter(cls.id == id).first()

        if candidate is None:
            return {'message': 'candidate not found'}, HTTPStatus.NOT_FOUND
        
        if data['name'] == '' or data['party'] == '':
            return {'message': "candidate's name and party must not be empty"}, HTTPStatus.NOT_FOUND
        
        if len(data['name']) < 3:
            return {'message': 'invalid name, name must be more than 3 characters !'}, HTTPStatus.BAD_REQUEST
        
        if len(data['party']) < 2:
            return {'message': 'invalid party name, it must be more than 2 characters !'}, HTTPStatus.BAD_REQUEST


        candidate.name = data['name']
        candidate.party = data['party']
        
        
        db.session.commit()
        return candidate.data, HTTPStatus.OK

    @classmethod
    def delete(cls, id):
        candidate = cls.query.filter(cls.id == id).first()
        if candidate is None:
            return {'message': 'candidate not found'}, HTTPStatus.NOT_FOUND

        db.session.delete(candidate)
        db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    @classmethod
    def publish(cls, candidate_id):
        candidate = Candidate.get_by_id_n(candidate_id)
        if candidate is None:
            return {'message': 'candidate not found'}, HTTPStatus.NOT_FOUND

        candidate.is_publish = True
        db.session.commit()
        return candidate.data, HTTPStatus.OK

    @classmethod
    def un_publish(cls, candidate_id):
        candidate = Candidate.get_by_id(candidate_id)
        if candidate is None:
            return {'message': 'candidate not found'}, HTTPStatus.NOT_FOUND

        candidate.is_publish = False
        db.session.commit()
        return candidate.data, HTTPStatus.OK
    
    def save(self):
        db.session.add(self)
        db.session.commit()
