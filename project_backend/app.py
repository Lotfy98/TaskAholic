from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Project, Task
from flask_restful import Api, reqparse
from resources import UserResource, ProjectResource, TaskResource
from flask_migrate import Migrate
import secrets
import pdb

app = Flask(__name__, template_folder='project_template',
            static_folder='project_template/style')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://taskaholic_dev:taskaholic_dev_pwd@localhost/taskaholic_dev_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
api = Api(app)

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


@app.route('/')
def home():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_post():
    import pdb
    pdb.set_trace()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Create a new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', projects=projects, tasks=tasks)


@app.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        description = request.form['description']

        new_project = Project(title=title, deadline=deadline,
                              description=description, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('projects.html')


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form['title']
        deadline = request.form['deadline']
        description = request.form['description']

        new_task = Task(title=title, deadline=deadline,
                        description=description, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('tasks.html')


api.add_resource(UserResource, '/api/users')
api.add_resource(ProjectResource, '/api/projects')
api.add_resource(TaskResource, '/api/tasks')

if __name__ == '__main__':
    app.run(debug=True)
