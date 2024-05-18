from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Project, Task
from app import app, db


def render_dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects, tasks=tasks)


def render_signup():
    return render_template('signup.html')


def render_login():
    return render_template('login.html')


@app.route('/')
def home():
    return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle POST request (form submission)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Create a new user and add it to the database
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_signup()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    return render_login()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_dashboard()


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
