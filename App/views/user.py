from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from App.models import Competition, CompetitonUser, User, db

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/home', methods=['GET'])
@login_required
def get_home_page():
    admin = current_user.is_admin
    competitions = Competition.query.all()
    return render_template("home.html", competitions=competitions, admin=admin)

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/', methods=['GET'])
def get_login_page():
    users = get_all_users()
    return render_template('login.html', users=users)

@user_views.route("/logout", methods=['GET'])
@login_required
def logout_action():
  logout_user()
  flash('Logged Out')
  return redirect(url_for('user_views.get_login_page'))

@user_views.route("/competition/<int:competition_id>", methods=['GET'])
@login_required
def get_desc(competition_id):
  competitions = Competition.query.all()
  compid = competition_id
  admin = current_user.is_admin

  return render_template("home.html", competitions=competitions, compid=compid, admin=admin)

@user_views.route("/addcompetition", methods=['GET'])
@login_required
def get_add_competition():
    is_adding = True
    is_editting = False
    return render_template('competition.html', is_adding=is_adding, is_editting=is_editting)

@user_views.route("/editcompetition/<int:competition_id>", methods=['GET'])
@login_required
def get_edit_competition(competition_id):
    compid = competition_id
    competitions = Competition.query.all()
    is_adding = False
    is_editting = True
    return render_template('competition.html', is_adding=is_adding, is_editting=is_editting, compid=compid, competitions=competitions)

@user_views.route('/signup', methods=['GET'])
def get_signup_page():
    users = get_all_users()
    return render_template('signup.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/', methods=['POST'])
def user_login_api():
    data = request.form
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        flash('Logged in successfully.')
        login_user(user)
        return redirect(url_for('user_views.get_home_page'))
    else:
        flash('Invalid username or password')
    return redirect('/')

@user_views.route("/signup", methods=['POST'])
def signup_action():
  data = request.form
  newuser = User(username=data['username'], password=data['password'], is_admin=False)
  try:
    db.session.add(newuser)
    db.session.commit()
    login_user(newuser)
    flash('Account Created!')
    return redirect(url_for('user_views.get_home_page'))
  except Exception:
    db.session.rollback()
    flash("Username or email already exists")
  return redirect(url_for('user_views.get_signup_page'))

@user_views.route("/addcompetition", methods=['POST'])
@login_required
def addcompetition():
    data = request.form
    newcomp = Competition(name=data['name'], category=data['category'], winner=data['winner'], runnerup=data['runnerup'], description=data['description'])
    db.session.add(newcomp)
    db.session.commit()
    flash('Competition added!')
    return redirect(url_for('user_views.get_home_page'))

@user_views.route("/editcompetition/<int:competition_id>", methods=['POST'])
@login_required
def editcompetition(competition_id):
    data = request.form
    compid = competition_id
    Competition.edit_competition(compid, data['name'], data['category'], data['winner'], data['runnerup'], data['description'])
    flash('Competiton editted!')

    admin = current_user.is_admin
    competitions = Competition.query.all()
    return render_template("home.html", competitions=competitions, admin=admin)

@user_views.route("/deletecompetition/<int:competition_id>", methods=['GET'])
@login_required
def removecompetition(competition_id):
    Competition.delete_competition(competition_id)

    admin = current_user.is_admin
    competitions = Competition.query.all()
    return render_template("home.html", competitions=competitions, admin=admin)
    
@user_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')