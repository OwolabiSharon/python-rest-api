import os
import hashlib

from flask import Flask, jsonify
from flask_restful import Api,Resource, reqparse
#from resources.user import Email
from flask_mail import *
from db import db
from models.user import User
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '!@#$%^&*()_+=-0987654321'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USE_SSL']= False
app.config['MAIL_DEBUG']= True
app.config['TESTING']=False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_USERNAME']='ubeussharexy@gmail.com'
app.config['MAIL_PASSWORD']='@#phone123'

api = Api(app)
mail = Mail(app)

users = []
numbers = ["345678900", "8899998777","788993545", '8765433456',"6547782","6367476426248","784748484747"]


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


class USER(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        numbers = ["345678900", "8899998777","788993545", '8765433456',"6547782","6367476426248","784748484747"]
        random_number = random.choice(numbers)
        global users

        data = USER.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        user = User(data['username'], data['password'],data['email'])
        users.append(user)

        message = Message('this is a verificatrion email from ubeus.sharexy.com' , sender ="iyowolabi@gmail.com",recipients =[user.email])
        message.body = "type in this to verify your email " + random_number + "God bless you as you do so"
        mail.send(message)


        #try:

        #except:
        #    return {'message':'something went wrong is your email valid bayi???'}


        return {"message": "User created successfully, verify your email, something as been sent to your email"}, 201





class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('verification_code',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )


    def post(self):
        global numbers
        global users
        data = Email.parser.parse_args()

        user = next(filter(lambda x: x.email == data['email'] , users))
        if user is None:
            return {'message':'what are you attempting'}
        if User.find_by_email(data['email']):
            return {"message": "A user with this email as already been verified and is saved in our database"}, 400

        elif data['verification_code'] in numbers and user.email == data['email']:
            encrypt_string(user.password)
            User.save_to_db(user)
            return {'message':'now you are verified and saved to our database'}
        return {'message':'you dont know what you are doing'}




class userList(Resource):
    global users
    def get(self):
        #return jsonify(users)
        return {'user': [x.json() for x in User.query.all()]}

api.add_resource(USER, '/register')
api.add_resource(Email, '/verify')
api.add_resource(userList, '/users')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
