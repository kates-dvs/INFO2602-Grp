from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    #competition = db.relationship('UserCompetition', backref='user')

    def __init__(self, username, password, is_admin):
        self.username = username
        self.set_password(password)
        self.is_admin = is_admin

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
    
    def save_competition(self, competition_id, name):
        comp = Competition.query.get(competition_id)
        if comp:
            try:
                competition = UserCompetition(self.id, competition_id, name)
                db.session.add(competition)
                db.session.commit()
                return competition
            except Exception:
                db.session.rollback()
                return None
            return None

    def rename_userdescription(self, competition_id, name):
        comp = UserCompetition.query.get(competition_id)
        if comp.user == self:
            comp.name = name
            db.session.add(comp)
            db.session.commit()
            return True
        return None

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

    def delete_competition(comp_id):
        comp = Competition.query.get(comp_id)
        db.session.delete(comp)
        db.session.commit()
        return True

    def edit_competition(comp_id, name, category, winner, runnerup, description):
        comp = Competition.query.get(comp_id)
        comp.name = name
        comp.category = category
        comp.winner = winner
        comp.runnerup = runnerup
        comp.description = description
        db.session.add(comp)
        db.session.commit()
        return True

