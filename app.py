from flask import Flask
from flask_restful import Api,Resource, reqparse
from resources.user import Email
from flask_mail import *
from db import db
from models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '!@#$%^&*()_+=-0987654321'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']='iyowolabi@gmail.com'
app.config['MAIL_PASSWORD']='temi1967'

api = Api(app)
mail = Mail(app)

@app.before_first_request
def create_table():
    db.create_all()

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
        users = []
        data = USER.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        user = User(data['username'],data['password'],data['email'])
        users.append(user)

        try:
            message = Message('type in this to verify your email "random" ', sender ="iyowolabi@gmail.com",recipients =[user.email])
            message.body = "na message be this"
            mail.send(message)
        except:
            return {'message':'something went wrong is your email valid bayi???'}


        return {"message": "User created successfully, verify your email, something as been sent to your email"}, 201

api.add_resource(USER, '/register')
api.add_resource(Email, '/verify')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)