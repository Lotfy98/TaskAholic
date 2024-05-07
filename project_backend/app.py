from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Project, Task
from flask import Flask
from flask_restful import Api
from resources import UserResource, ProjectResource, TaskResource
from flask_migrate import Migrate



app = Flask(__name__, template_folder='project_template',
            static_folder='project_template/style')
app.config['SECRET_KEY'] = 'randomly_generated_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db'

db = SQLAlchemy(app) 
# Initialize SQLAlchemy
migrate = Migrate(app, db)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def homepage():
    return render_template('base.html')


@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Create a new user
        new_user = User( email=email, password=password)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('profile'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('base.html')
  # Redirect to homepage after logout


api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(ProjectResource, '/projects', '/projects/<int:project_id>')
api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')
# Run the application if this file is executed directly
    # Create database tables
with app.app_context():
    db.create_all()
if __name__ == '__main__':

    # Run the Flask app in debug mode
    app.run(debug=True)
