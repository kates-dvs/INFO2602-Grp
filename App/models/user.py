from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

db = SQLAlchemy()

class CompetitonUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    competition = db.relationship('Competition')
    name = db.Column(db.String(120), unique=True)
    winner = db.Column(db.Boolean, default=False)

    def __init__ (self, user_id, competition_id, name):
        self.user_id = user_id
        self.competition_id = competition_id
        self.name = name

    def __repr__(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'competition id' : self.competition_id,
            'competition' : self.competition,
            'winner' : self.winner
        }

    def get_winner(self):
        self.winner = not self.winner
        db.session.add(self)
        db.session.commit()

     def __repr__(self):
        return f'<Competition: {self.id} | {self.user.username} | {self.competition.comp_name} {"winner" if self.winner else "not winner"}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    competition = db.relationship('UserCompetition', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('CompetitionUser.id'), nullable=False)
    comp_name = db.Column(db.String(300), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    upcoming_comp = db.Column(db.String(300), nullable=False)

    def __init__ (self, id):
        self.id = id

    def toggle(self):
        self.completed = not self.completed
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f'<Competition: {self.id} | {self.user.username} | {self.comp_name} | {"completed" if self.completed else "in progress"}>'

    