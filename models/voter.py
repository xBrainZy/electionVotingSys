import sys
from extensions import db
from resources.user import UserListResource
from models.user import User
from http import HTTPStatus

import datetime as dt
from datetime import datetime, date, timedelta

class Validate:
    @classmethod
    def dateCaster(cls, str):
        date_object = datetime.strptime(str, '%Y-%m-%d').date() # convert string to date

        return date_object

    @classmethod
    def ageCalculator(cls, str):

        birth_date = cls.dateCaster(str)

        current_date = date.today()
                # days                    //  365.24.25(includes leap year)     =  age 
        age = (current_date - birth_date) // timedelta(days=365.2425) 


        if age > 17:

            return True
    
        return False

class Voter(db.Model):
    __tablename__ = 'voter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.DateTime(), nullable=False)
    
    is_publish = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.current_date())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), unique=True)

    ballots = db.relationship('Ballot', backref='voter')

    @property
    def data(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'DOB': dt.date.isoformat(self.dob),
            'User': User.get_name_by_id(self.user_id)
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
    def get_by_id_n(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_publish == False)).first()
        return x
    
    @classmethod
    def get_name_by_id(cls, voter_id):
        return cls.query.filter_by(id=voter_id).first().name

    @classmethod
    def update(cls, id, data):
        voter = cls.query.filter(cls.id == id).first()

        if voter is None:
            return {'message': 'voter not found'}, HTTPStatus.NOT_FOUND
        
        if data['name'] == '' or data['address'] == '' or data['DOB'] == '':
            return {'message': "voter's name, address and the date of birth must not be empty"}, HTTPStatus.NOT_FOUND
        
        if len(data['name']) < 3:
            return {'message': 'invalid name, name must be more than 3 characters !'}, HTTPStatus.BAD_REQUEST
        
        if ((len(data['address']) < 3) or (',' not in data['address']) ):
            return {'message': 'invalid location, name must be more than 3 characters !'}, HTTPStatus.BAD_REQUEST
        
        if not Validate.ageCalculator(data['DOB']):
            return {'message': "Voter's age must be 18 or older to be eligible to vote"}
        
        

        voter.name = data['name']
        voter.address = data['address']
        voter.dob = data['DOB']
        
        db.session.commit()
        return voter.data, HTTPStatus.OK

    @classmethod
    def delete(cls, id):
        voter = cls.query.filter(cls.id == id).first()
        if voter is None:
            return {'message': 'voter not found'}, HTTPStatus.NOT_FOUND

        db.session.delete(voter)
        db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    @classmethod
    def publish(cls, recipe_id):
        voter = Voter.get_by_id_n(recipe_id)
        if voter is None:
            return {'message': 'voter not found'}, HTTPStatus.NOT_FOUND

        voter.is_publish = True
        db.session.commit()
        return voter.data, HTTPStatus.OK

    @classmethod
    def un_publish(cls, recipe_id):
        voter = Voter.get_by_id(recipe_id)
        if voter is None:
            return {'message': 'voter not found'}, HTTPStatus.NOT_FOUND

        voter.is_publish = False
        db.session.commit()
        return voter.data, HTTPStatus.OK
    

    def save(self):
        db.session.add(self)
        db.session.commit()
