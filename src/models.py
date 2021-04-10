from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    favorites = db.relationship('Favorite', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "favorites": list(map(lambda x: x.serialize(), self.favorites)),
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category= db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "category": self.category,
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(30))
    gender = db.Column(db.String(30))
    height = db.Column(db.Integer)
    birth_year = db.Column(db.String(30))
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(30))
    skin_color = db.Column(db.String(30))
    eye_color = db.Column(db.String(30))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "gender": self.gender,
            "height": self.height,
            "birth_year": self.birth_year,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(30))
    climate = db.Column(db.String(30))
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.String(30))
    terrain = db.Column(db.String(30))
    surface_water = db.Column(db.Integer)
    population = db.Column(db.Integer)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
        }
