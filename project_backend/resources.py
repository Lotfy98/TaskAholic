from flask_restful import Resource, reqparse, Api
from models import db, User, Project, Task


api = Api()


parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True,
                    help='Username cannot be blank')
parser.add_argument('email', type=str, required=True,
                    help='Email cannot be blank')
parser.add_argument('password', type=str, required=True,
                    help='Password cannot be blank')
parser.add_argument('role', type=str, required=True,
                    help='Role cannot be blank')
parser.add_argument('title', type=str, required=True,
                    help='Title cannot be blank')
parser.add_argument('deadline', type=int, required=True,
                    help='Deadline cannot be blank')
parser.add_argument('description', type=str, required=True,
                    help='Description cannot be blank')


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return {'users': [user.username for user in users]}

    def post(self):
        args = parser.parse_args()
        new_user = User(
            username=args['username'], email=args['email'], password=args['password'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': f"User {new_user.username} has been created successfully"}, 201


class ProjectResource(Resource):
    def get(self):
        projects = Project.query.all()
        return {'projects': [project.title for project in projects]}

    def post(self):
        args = parser.parse_args()
        new_project = Project(title=args['title'], deadline=args['deadline'],
                              description=args['description'], owner_id=args['owner_id'])
        db.session.add(new_project)
        db.session.commit()
        return {'message': f"Project {new_project.title} has been created successfully"}, 201


class TaskResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return {'tasks': [task.title for task in tasks]}

    def post(self):
        args = parser.parse_args()
        new_task = Task(title=args['title'], deadline=args['deadline'],
                        description=args['description'], project_id=args['project_id'])
        db.session.add(new_task)
        db.session.commit()
        return {'message': f"Task {new_task.title} has been created successfully"}, 201
