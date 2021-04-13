"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
import json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('FLASK_APP_KEY')
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email, password=password).first()

    if user is None:
         return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)
    

# USER CRUD    


@app.route('/user', methods=['GET'])
@jwt_required()
def handle_user():

    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    return jsonify(user.serialize()), 200


@app.route('/user/<int:id>', methods=['GET'])
def handle_single_user(id):
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    return jsonify(user.serialize()), 200


@app.route('/user', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(email=body["email"], username=body["username"], password=body["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(body), 200


# CHARACTER CRUD    


@app.route('/character', methods=['GET'])
def handle_character():
    characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), characters))
    return jsonify(all_characters), 200


@app.route('/character', methods=['POST'])
def create_character():
    body = request.get_json()
    new_character = Character(name=body["name"], gender=body["gender"], height=body["height"], birth_year=body["birth_year"], mass=body["mass"], hair_color=body["hair_color"], skin_color=body["skin_color"], eye_color=body["eye_color"])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(body), 200


# PLANET CRUD    


@app.route('/planet', methods=['GET'])
def handle_planet():
    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))
    return jsonify(all_planets), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(name=body["name"], climate=body["climate"], diameter=body["diameter"], gravity=body["gravity"], terrain=body["terrain"], surface_water=body["surface_water"], population=body["population"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(body), 200


# FAVORITE CRUD   


@app.route('/favorite', methods=['GET'])
def handle_favorite():
    favorites = Favorite.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify(all_favorites), 200

@app.route('/favorite', methods=['POST'])
@jwt_required()
def create_favorite():
    current_user = get_jwt_identity()
    body = request.get_json()
    new_favorite = Favorite(name=body["name"], category=body["category"], user_id=body["user_id"])
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(body), 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(id):
    current_user = get_jwt_identity()
    favorite = Favorite.query.get(id)
    if favorite is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    response = { "msg" : "Favorite deleted successfully" }
    return jsonify(response), 200





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
