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
from models import db, User, Character, Planet
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/character', methods=['GET'])
def handle_character():
    return jsonify(Character.get_characters()), 200

@app.route('/character', methods=['POST'])
def create_character():
    body = request.get_json()
    new_character = Character(name=body["name"], gender=body["gender"], height=body["height"], birth_year=body["birth_year"], mass=body["mass"], hair_color=body["hair_color"], skin_color=body["skin_color"], eye_color=body["eye_color"])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(body), 200

@app.route('/planet', methods=['GET'])
def handle_planet():
    return jsonify(Planet.get_planets()), 200

@app.route('/planet', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(name=body["name"], climate=body["climate"], diameter=body["diameter"], gravity=body["gravity"], terrain=body["terrain"], surface_water=body["surface_water"], population=body["population"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
