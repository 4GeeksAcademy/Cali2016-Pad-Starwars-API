"""
This module starts the API Server, loads the DB and adds the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

# Database configuration
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# ❗ Error handler
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# ❗ Sitemap
@app.route("/")
def sitemap():
    return generate_sitemap(app)


# ----------------------------
#       PEOPLE ENDPOINTS
# ----------------------------

@app.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200


@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200


# ----------------------------
#       PLANET ENDPOINTS
# ----------------------------

@app.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


# ----------------------------
#       USER ENDPOINTS
# ----------------------------

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    # For now, use HARD-CODED user 1
    user = User.query.get(1)
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=1).all()
    return jsonify([fav.serialize() for fav in favorites]), 200


# ----------------------------
#       FAVORITES (PLANETS)
# ----------------------------

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    new_fav = Favorite(user_id=1, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    fav = Favorite.query.filter_by(user_id=1, planet_id=planet_id).first()
    if fav is None:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200


# ----------------------------
#       FAVORITES (PEOPLE)
# ----------------------------

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    new_fav = Favorite(user_id=1, people_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"msg": "Person added to favorites"}), 200


@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    fav = Favorite.query.filter_by(user_id=1, people_id=people_id).first()
    if fav is None:
        return jsonify({"msg": "Favorite person not found"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"msg": "Favorite person deleted"}), 200


# Run server
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True
    )
