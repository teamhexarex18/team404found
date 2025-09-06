from EmailOtp import sendOTP 
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from datetime import time, timedelta
from google import genai
from flask import Flask, request, redirect as rd, render_template as rt, session, flash, jsonify
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
import pymysql
import json
import os
from flask_cors import CORS


pymysql.install_as_MySQLdb()


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ODOO'
app.permanent_session_lifetime = timedelta(minutes=30) 
app.secret_key = '1234567890qwertyuiopasdfghjklzxcvbnm789456123'
client = genai.Client(api_key='AIzaSyCpaiaZyNTU3InO6zJPANpJqphn1OMEU1I')
db = SQLAlchemy(app)
CORS(app) 
class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    otpcorrect = db.Column(db.Integer, default=0)

class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True) 
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    priority = db.Column(db.Integer, nullable=False)

class ProjectMembers(db.Model):
    __tablename__ = 'project_members'
    member_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    role = db.Column(db.String(100), nullable=False)

class Tasks(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    image_url = db.Column(db.String(255), default=None)
    task_name = db.Column(db.String(100), nullable=False)
    task_description = db.Column(db.String(255), nullable=False)
    assigned_to_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(100), nullable=False,default=TaskStatus.PENDING)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


@app.route('/')
def root():
    if 'user_id' not in session:
        return rd('/login')
    return rd('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user == None:
            return rd('/register?ue=T')


        if user and cph(user.password, password):
            session['user_id'] = user.user_id
            session['name'] = user.name
            session.permanent=True
            return rd('/home')

    return rt('login.html',message='USER EXISTS') if 'ue' in request.args else rt('login.html', message='USER NOT EXISTS')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        if User.query.filter_by(email=email).first():
            return rd('/login?ue=1')


        otp = sendOTP(email)

        session['pending_user'] = {
            "name": name,
            "email": email,
            "password": password,
            "otp": otp
        }

        return rd('/verify-otp')
    return rt('register.html')

# ---------------- Registration OTP ----------------

# ---------------- Registration OTP ----------------
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    pending_user = session.get('pending_user')

    if not pending_user:
        flash("Session expired. Please try again.")
        return rd('/register')

    if request.method == "POST":
        otp_entered = request.form.get('otp', '').strip()
        if not otp_entered:
            flash("Please enter the OTP.")
            return rt('verify-otp.html')

        if otp_entered == str(pending_user['otp']):
            raw_password = pending_user.get('password')
            if not raw_password:
                flash("Error: Password missing. Please register again.")
                return rd('/register')

            new_user = User(
                name=pending_user.get('name'),
                email=pending_user.get('email'),
                password=gph(raw_password),
                otp=pending_user.get('otp'),
                otpcorrect=1
            )
            db.session.add(new_user)
            db.session.commit()
            session.pop('pending_user', None)
            flash("OTP verified successfully. Please login.")
            return rd('/login')
        else:
            flash("Invalid OTP. Try again.")
            return rt('verify-otp.html')

    return rt('verify-otp.html')


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    pending_user = session.get('pending_user')

    # If session expired → force user to start again
    if not pending_user:
        flash("Session expired. Please request password reset again.")
        return rd('/forget-password')

    if request.method == "POST":
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not new_password or not confirm_password:
            flash("Please fill in both fields.")
            return rt('reset-password.html')

        if new_password != confirm_password:
            flash("Passwords do not match.")
            return rt('reset-password.html')

        # Update password in database
        user = User.query.filter_by(email=pending_user['email']).first()
        if user:
            user.password = gph(new_password)  # Hash the new password
            db.session.commit()

            # Clear session so it doesn’t get reused
            session.pop('pending_user', None)

            flash("Password reset successful. Please login.")
            return rd('/login')
        else:
            flash("User not found. Please register.")
            return rd('/register')

    return rt('reset-password.html')

@app.route('/verify-fp', methods=['GET', 'POST'])
def verify_otp_fp():
    pending_user = session.get('pending_user')

    if not pending_user:
        flash("Session expired. Please try again.")
        return rd('/forget-password')

    if request.method == "POST":
        otp_entered = request.form.get('otp', '').strip()
        if not otp_entered:
            flash("Please enter the OTP.")
            return rt('verify-otp-fp.html')

        if otp_entered == str(pending_user['otp']):
            flash("OTP verified. Please reset your password.")
            return rd('/reset-password')
        else:
            flash("Invalid OTP for password reset. Try again.")
            return rt('verify-otp-fp.html')

    return rt('verify-otp-fp.html')








@app.route('/home', methods=['GET'])
def home():
    if 'user_id' not in session:
        return rd('/login')
    
    user_id = session['user_id']
    user = User.query.filter_by(user_id=user_id).first()
    projects = Project.query.all()
    tasks = Tasks.query.all()

    
    return rt('home.html', user=user, projects=projects, tasks=tasks)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return rd('/')


@app.route('/projects/add', methods=['GET', 'POST'])
def add_project():
    if 'user_id' not in session:
        flash("Login required")
        return rd('/login')

    if request.method == 'POST':
        # Get data from form
        name = request.form.get('name')
        description = request.form.get('description')
        priority = int(request.form.get('priority', 1))  # Default priority
        image = request.files.get('image')
        image_url = None

        # Handle image upload
        if image and image.filename:
            uploads_dir = os.path.join(app.root_path, 'static/uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            filename = f"{int(time.time())}_{image.filename}"
            image_path = os.path.join(uploads_dir, filename)
            image.save(image_path)
            image_url = f"uploads/{filename}"  # save relative path in DB

        try:
            project = Project(
                project_name=name,
                project_description=description,
                created_by=session['user_id'],
                priority=priority
            )
            db.session.add(project)
            db.session.commit()
            flash("Project created successfully!")
            return rd('/home')
        except Exception as e:
            flash(f"Error: {str(e)}")
            return rt('add-project.html')

    # GET request → render the add project form
    return rt('add-project.html')




@app.route('/projects', methods=['GET'])
def get_projects():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    projects = Project.query.filter_by(created_by=session['user_id']).all()
    return jsonify([{
        "project_id": p.project_id,
        "name": p.project_name,
        "description": p.project_description,
        "priority": p.priority,
        "created_at": str(p.created_at)
    } for p in projects])

@app.route('/projects/update/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    project = Project.query.filter_by(project_id=project_id, created_by=session['user_id']).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    data = request.json
    project.project_name = data.get('name', project.project_name)
    project.project_description = data.get('description', project.project_description)
    project.priority = data.get('priority', project.priority)
    db.session.commit()
    return jsonify({"message": "Project updated"})

@app.route('/projects/delete/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    project = Project.query.filter_by(project_id=project_id, created_by=session['user_id']).first()
    if not project:
        return jsonify({"error": "Project not found"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})


# ------------------- TASK CRUD ENDPOINTS -------------------
from datetime import date 


@app.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    if 'user_id' not in session:
        flash("Login required")
        return rd('/login')

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        name = request.form.get('name')
        description = request.form.get('description')
        assignee = request.form.get('assignee')
        deadline = request.form.get('deadline')
        image = request.form.get('image')

        try:
            task = Tasks(
                project_id=project_id,
                task_name=name,
                task_description=description,
                assigned_to_user_id=assignee,
                due_date=date.fromisoformat(deadline),
                status=TaskStatus.PENDING.value,
                image_url=image
            )
            db.session.add(task)
            db.session.commit()
            flash("Task created successfully!")
            return rd('/home')
        except Exception as e:
            flash(f"Error: {str(e)}")
            return rt('add-task.html')

    return rt('add-task.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    tasks = Tasks.query.filter_by(assigned_to_user_id=session['user_id']).all()
    return jsonify([{
        "task_id": t.task_id,
        "name": t.task_name,
        "description": t.task_description,
        "status": t.status,
        "deadline": str(t.due_date),
        "project_id": t.project_id,
        "image_url": t.image_url
    } for t in tasks])

@app.route('/tasks/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    task = Tasks.query.filter_by(task_id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    task.task_name = data.get('name', task.task_name)
    task.task_description = data.get('description', task.task_description)
    task.assigned_to_user_id = data.get('assignee', task.assigned_to_user_id)
    task.project_id = data.get('project_id', task.project_id)
    task.image_url = data.get('image', task.image_url)
    if 'deadline' in data:
        task.due_date = date.fromisoformat(data['deadline'])
    task.status = data.get('status', task.status)
    db.session.commit()
    return jsonify({"message": "Task updated"})

@app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    task = Tasks.query.filter_by(task_id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})


@app.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account found with that email.")
            return rd('/forget-password')

        otp = sendOTP(email)
        session['pending_user'] = {"email": email, "otp": otp}
        return rd('/verify-fp')   

    return rt('forget-password.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


