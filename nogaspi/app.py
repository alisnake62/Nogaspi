from flask import Flask, jsonify, request
import secrets
import datetime
from zoneinfo import ZoneInfo
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.sql.sqltypes import DATE, INTEGER, TEXT, VARCHAR, String
from sqlalchemy.orm import relationship, sessionmaker
import json
Base = declarative_base()

def apiResponse(request, data = None, exception : bool = False, code = 200):
    
    if exception: summary = "Exception"
    else : summary = "Ok"
    
    metadata = {
        'url': request.url,
        'method' : request.method,
        'inputJson': request.json,
        'summary': summary,
        'code': code
    }
    json = {
        'metadata': metadata,
        'data': data
    }

    return jsonify(json)

class APIException(Exception):
    status_code = 400

    def __init__(self, message, request, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.request = request
        if status_code is not None:
            self.status_code = status_code

    def response(self):
        data = {
            'exception' : self.__class__.__name__,
            'message' : self.message
        }
        return apiResponse(request = self.request, data=data, exception=True, code=self.status_code)

class LoginException(APIException):
    pass

class DBException(APIException):
    pass

class TokenException(APIException):
    pass

class EmptyException(APIException):
    pass


class User (Base):

    TOKEN_VALIDITY = 15   #minutes

    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True)
    mail = Column(VARCHAR)
    password = Column(VARCHAR)
    token = Column(VARCHAR)
    token_expiration = Column(DATE)

    def __init__(self, mail : String, password : String):                    
        self.mail = mail             
        self.password = password

    def generateToken(self):
        self.token = secrets.token_hex()
        self.token_expiration = datetime.datetime.now() + datetime.timedelta(minutes = self.TOKEN_VALIDITY)
        return {'token': self.token, 'token_expiration': str(self.token_expiration + datetime.timedelta(minutes = 60)) + " GMT+1"}


class Article (Base):

    __tablename__ = 'article'
    id = Column(INTEGER, primary_key=True)
    opinion = Column(TEXT)
    brand = Column(VARCHAR)
    name = Column(VARCHAR)
    quantity = Column(VARCHAR)
    barcode = Column(VARCHAR)
    image_url = Column(VARCHAR)

    def __init__(self, name, quantity, opinion=None, brand=None, barcode=None, image_url=None):                    
        self.opinion = opinion        
        self.brand = brand
        self.name = name
        self.quantity = quantity
        self.barcode = barcode
        self.image_url = image_url

app = Flask(__name__)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = error.response()
    response.status_code = error.status_code
    return response


@app.route('/register/login', methods=['POST'])
def login():

    try:
        password = os.environ['MYSQL_ROOT_PASSWORD']

        engine = create_engine('mysql+mysqlconnector://root:{}@db_nogaspi/nogaspi'.format(password), echo=False)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        
    except Exception as e:
        print(type(e), e)
        raise DBException("problem to access at tha database", request)

    try:
        mail = request.json['mail']
        password = request.json['password']
        user = session.query( User ).filter(User.mail == mail).first()

        if (user.password != password): raise LoginException("login / password incorrect", request)
        
    
    except Exception as e:
        print(type(e), e)
        raise LoginException("login / password incorrect", request)

    
    try:
        tokenInfo = user.generateToken()
        session.commit()
        
    except Exception as e:
        print(type(e), e)
        raise TokenException("problem to generate token", request)

    return apiResponse(request, tokenInfo)

@app.route('/test', methods=['GET'])
def test():

    data = {"toto":  ["tata", "titi"]}

    return apiResponse(request=request, data=data)


@app.route('/getUsers', methods=['GET'])
def getUsers():


    engine = create_engine('mysql+mysqlconnector://root:nogaspiPwd@db_nogaspi/nogaspi', echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    users = session.query( User )
    
    test = [u.mail + " : " + u.password for u in users]
    return jsonify(test)

@app.route('/getArticle', methods=['GET'])
def getArticle():

    
    try:
        
        password = os.environ['MYSQL_ROOT_PASSWORD']

        engine = create_engine('mysql+mysqlconnector://root:{}@db_nogaspi/nogaspi'.format(password), echo=False)
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        
    except Exception as e:
        print(type(e), e)
        raise DBException("problem to access at tha database", request)

    ### verify token
    token = request.json['token']
    user = session.query( User ).filter(User.token == token).first()

    if not user:
        raise LoginException("Token incorrect", request)
    elif user.token_expiration < datetime.datetime.now():
        raise LoginException("Token expired", request)

    # maj date token
    barcode = token = request.json['barcode']

    article = session.query( Article ).filter(Article.barcode == barcode).first()

    if not article:
        raise EmptyException("No article with this barcode", request)

    data = {
        'opinion': article.opinion,
        'name': article.name,
        'brand': article.brand,
        'quantity': article.quantity,
        'barcode': article.barcode,
        'image_url': article.image_url
    }
    

    return apiResponse(request, data)


if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0")
