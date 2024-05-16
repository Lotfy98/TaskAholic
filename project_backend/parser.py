from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, help='This field cannot be blank')
parser.add_argument('email', type=str, help='This field cannot be blank')
parser.add_argument('password', type=str, help='This field cannot be blank')
