from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, User, Project, Task

# Define request parsers
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str,
                         required=True, help='Username is required')
user_parser.add_argument(
    'email', type=str, required=True, help='Email is required')

project_parser = reqparse.RequestParser()
project_parser.add_argument(
    'title', type=str, required=True, help='Title is required')
project_parser.add_argument('description', type=str)

task_parser = reqparse.RequestParser()
task_parser.add_argument(
    'title', type=str, required=True, help='Title is required')
task_parser.add_argument('description', type=str)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

project_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'user_id': fields.Integer
}

task_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'project_id': fields.Integer
}

# Resource for managing users


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user, 201

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

# Resource for managing projects


class ProjectResource(Resource):
    @marshal_with(project_fields)
    def get(self, project_id):
        project = Project.query.get_or_404(project_id)
        return project

    @marshal_with(project_fields)
    def post(self):
        args = project_parser.parse_args()
        project = Project(**args)
        db.session.add(project)
        db.session.commit()
        return project, 201

    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return '', 204

# Resource for managing tasks


class TaskResource(Resource):
    @marshal_with(task_fields)
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return task

    @marshal_with(task_fields)
    def post(self):
        args = task_parser.parse_args()
        task = Task(**args)
        db.session.add(task)
        db.session.commit()
        return task, 201

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
