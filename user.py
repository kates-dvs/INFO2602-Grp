from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

#db = SQLAlchemy()

class CompetitonUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))
    competition = db.relationship('Competition')
    name = db.Column(db.String(120), unique=True)

    def __init__ (self, user_id, competition_id, name):
        self.user_id = user_id
        self.competition_id = competition_id
        self.name = name

    def __repr__(self):
        return f'<Competition: {self.id} | {self.name} | {self.user.username}>'

    def __repr__(self):
        return{
            'id' : self.id,
            'name' : self.name,
            'competition id' : self.competition.id,
            'competition' : self.competition.name,
            'category' : self.competition.category,
            'winner' : self.competition.winner,
            'runner up' : self.competition.runnerup,
            'description' : self.competition.description
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    #competition = db.relationship('UserCompetition', backref='user')

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
    name = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    winner = db.Column(db.String(255), nullable=False)
    runnerup = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    def get_json(self):
        return{
            'competition_id': self.id,
            'name' : self.name,
            'category' : self.category,
            'winner' : self.winner,
            'runner up' : self.runnerup,
            'description': self.description
        }