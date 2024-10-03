
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import insert_user, get_users, get_user_by_id, update_user, delete_user, create_db_table

app = Flask(__name__)
CORS(app)

# Create the database and table on the first run
create_db_table()  # This will ensure the 'users.db' file is created and the table is set up

# Add a root route to avoid 404 errors when accessing the base URL
@app.route('/')
def home():
    return "<h1>Welcome to the Flask User Management API!</h1><p>Use /api/users to interact with the API.</p>"

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
