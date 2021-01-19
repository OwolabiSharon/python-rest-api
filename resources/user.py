from db import db
from models.user import User
from flask_restful import Resource, reqparse
from flask_mail import *

class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('verification_code',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
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
        data = Email.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message": "this user as already been verified and is saved in our database"}, 400
        elif data['verification_code'] == 'random':
            user = User(data['username'],data['password'],data['email'])
            User.save_to_db(user)
        return {'message':'now you are verified and saved to our database'}
