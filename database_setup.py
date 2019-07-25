from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import random, string

Base = declarative_base()

# creating a secret key
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) 
for x in range(32))

    
# User Class
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    hash_password = Column(String(64))

    # constructor
    def __init__(self, username,email,password):
        self.username = username
        self.email = email
        self.hash_password = generate_password_hash(password)

    # verify password function
    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    # generating auth token 10min = 600seconds of expiration time
    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(secret_key, expires_in = expiration)
    #     return s.dumps({'id': self.id })

    # @staticmethod
    # def verify_auth_token(token):
    # 	s = Serializer(secret_key)
    # 	try:
    # 		data = s.loads(token)
    # 	except SignatureExpired:
    # 		#Valid Token, but expired
    # 		return None
    # 	except BadSignature:
    # 		#Invalid Token
    # 		return None
    # 	user_id = data['id']
    # 	return user_id


# Category Class
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'description': self.description
           
       }


# Items Class
class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
 
Base.metadata.create_all(engine)

