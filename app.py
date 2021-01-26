from flask import Flask
from flask_restful import Api,Resource, reqparse
from resources.user import Email
from flask_mail import *
from db import db
from models.user import User
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '!@#$%^&*()_+=-0987654321'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USE_SSL']= False
app.config['MAIL_DEBUG']= True
app.config['TESTING']=False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_USERNAME']='sharexy23@gmail.com'
app.config['MAIL_PASSWORD']='@#phone123'

api = Api(app)
mail = Mail(app)


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
        users = []
        data = USER.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400
        user = User(data['username'],data['password'],data['email'])
        users.append(user)

        message = Message('type in this to verify your email ' + random_number +'God bless you as you do so' , sender ="iyowolabi@gmail.com",recipients =[user.email])
        message.body = "na message be this"
        mail.send(message)

        #try:

        #except:
        #    return {'message':'something went wrong is your email valid bayi???'}


        return {"message": "User created successfully, verify your email, something as been sent to your email"}, 201

api.add_resource(USER, '/register')
api.add_resource(Email, '/verify')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
