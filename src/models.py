from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(String(80), nullable=False)
    is_active = db.Column(Boolean(), nullable=False)

    favorites = db.relationship("Favorite", backref="user", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(120), nullable=False)
    height = db.Column(String(20))
    gender = db.Column(String(20))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender
        }


class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(120), nullable=False)
    climate = db.Column(String(120))
    population = db.Column(Integer)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }


class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Optional fields — user can favorite a planet OR a person
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)

    planet = db.relationship("Planet", lazy=True)
    people = db.relationship("People", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None,
            "people": self.people.serialize() if self.people else None
        }
