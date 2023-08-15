from extensions import db
from http import HTTPStatus
# User Attributes
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    voters = db.relationship('Voter', backref='user')

    @property
    def data(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    @classmethod
    def get_all(cls):
        r = cls.query.filter_by(is_active=True).all()

        result = []

        for i in r:
            result.append(i.data)

        return result
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter((cls.id == id) & (cls.is_active == True)).first()
    
    @classmethod
    def get_by_id_n(cls, id):
        x = cls.query.filter((cls.id == id) & (cls.is_active == False)).first()
        return x


    # A static method to get a user data by the username
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # A static method to get a user data by the email
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # A static method to get a user data by the id
    @classmethod
    def get_name_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first().username
    
    @classmethod
    def update(cls, id, data):
        user = cls.query.filter(cls.id == id).first()

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        
        # Do not add the user if the username is taken
        if User.get_by_username(data['username']):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        # Do not add the user if the email is taken
        if User.get_by_email(data['email']):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        if len(data['username']) < 2:
            return {'message': 'invalid username, username must be more than 2 characters !'}, HTTPStatus.BAD_REQUEST
        
        if '@' not in data['email']:
            return {'message': 'invalid email'}, HTTPStatus.BAD_REQUEST

        user.username = data['username']
        user.email = data['email']

        
        db.session.commit()
        return user.data, HTTPStatus.OK
    

    @classmethod
    def publish(cls, user_id):
        user = User.get_by_id_n(user_id)
        if user is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        user.is_publish = True
        db.session.commit()
        return user.data, HTTPStatus.OK

    @classmethod
    def un_publish(cls, user_id):
        user = User.get_by_id(user_id)
        if user is None:
            return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

        user.is_active = False
        db.session.commit()
        return user.data, HTTPStatus.OK

    # Save the record
    def save(self):
        db.session.add(self)
        db.session.commit()