from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.json or not 'id' in request.json:
        abort(400)
    new_picture = {
        "id": request.json['id'],
        "event_city": request.json.get('event_city', ""),
        "event_country": request.json.get('event_country', ""),
        "event_date": request.json.get('event_date', ""),
        "event_state": request.json.get('event_state', ""),
        "event_type": request.json.get('event_type', ""),
        "image": request.json.get('image', ""),
        "image_type": request.json.get('image_type', ""),
        "poster_email": request.json.get('poster_email', ""),
        "poster_name": request.json.get('poster_name', ""),
        "poster_organization": request.json.get('poster_organization', "")
    }
    if any(picture['id'] == new_picture['id'] for picture in data):
        return jsonify({"message": f"Picture with id {new_picture['id']} already present"}), 302
    data.append(new_picture)
    with open(json_url, 'w') as f:
        json.dump(data, f)
    return jsonify(new_picture), 201

######################################################################
# CREATE A PICTURE WITH ID
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture_with_id(id):
    if not request.json:
        abort(400)
    new_picture = {
        "id": id,
        "event_city": request.json.get('event_city', ""),
        "event_country": request.json.get('event_country', ""),
        "event_date": request.json.get('event_date', ""),
        "event_state": request.json.get('event_state', ""),
        "event_type": request.json.get('event_type', ""),
        "image": request.json.get('image', ""),
        "image_type": request.json.get('image_type', ""),
        "poster_email": request.json.get('poster_email', ""),
        "poster_name": request.json.get('poster_name', ""),
        "poster_organization": request.json.get('poster_organization', "")
    }
    if any(picture['id'] == new_picture['id'] for picture in data):
        return jsonify({"message": f"Picture with id {new_picture['id']} already present"}), 302
    data.append(new_picture)
    with open(json_url, 'w') as f:
        json.dump(data, f)
    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    picture.update(request.json)
    with open(json_url, 'w') as f:
        json.dump(data, f)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404
    data = [item for item in data if item["id"] != id]
    with open(json_url, 'w') as f:
        json.dump(data, f)
    return {"message": "Picture deleted"}, 200