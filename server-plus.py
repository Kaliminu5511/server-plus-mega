from flask import Flask, request, jsonify, send_from_directory, redirect
import os
import json

app = Flask(__name__)

users = {}
groups = {}

@app.route('/')
def index():
    return redirect('/groups.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('web', path)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    if username not in users:
        users[username] = {"groups": []}
    return jsonify({"success": True, "username": username})

@app.route('/create_group', methods=['POST'])
def create_group():
    group_name = request.form.get('group_name')
    if group_name and group_name not in groups:
        groups[group_name] = {"members": []}
    return jsonify({"success": True, "group": group_name})

@app.route('/join_group', methods=['POST'])
def join_group():
    username = request.form.get('username')
    group_name = request.form.get('group_name')
    if username and group_name:
        if group_name in groups and username not in groups[group_name]["members"]:
            groups[group_name]["members"].append(username)
            users[username]["groups"].append(group_name)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route('/groups', methods=['GET'])
def list_groups():
    return jsonify({"groups": list(groups.keys())})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
