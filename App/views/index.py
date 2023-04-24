from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, Competition, CompetitonUser, User
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def login_page():
    users = get_all_users()
    return render_template('login.html', users=users)

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')

    with open('competitions.csv', newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            competition = Competition(name=row['name'], category=row['category'], winner=row['winner'], runnerup=row['runnerup'], description=row['description'])
            db.session.add(competition)
        db.session.commit()
    flash('database initalized')
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
