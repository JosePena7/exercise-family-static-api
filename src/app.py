"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# GET all members
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    result = []
    for m in members:
        m_copy = m.copy()
        if "name" in m_copy:
            m_copy["first_name"] = m_copy.pop("name")
        result.append(m_copy)
    return jsonify(result), 200


# GET single member
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        member_copy = member.copy()
        if "name" in member_copy:
            member_copy["first_name"] = member_copy.pop("name")
        return jsonify(member_copy), 200
    return jsonify({"error": "Member not found"}), 404


# POST new member
@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()
    if not body:
        return jsonify({"error": "Invalid JSON"}), 400

    new_member = jackson_family.add_member({
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"],
    })

    response_member = new_member.copy()
    if "name" in response_member:
        response_member["first_name"] = response_member.pop("name")

    return jsonify(response_member), 200


# DELETE member
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if deleted:
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
