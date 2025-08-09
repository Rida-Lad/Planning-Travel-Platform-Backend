from flask import Blueprint, jsonify
from app.services.database import Database

activities_bp = Blueprint('activities', __name__)
db = Database()

@activities_bp.route('/api/activity-options', methods=['GET'])
def get_activity_options():
    try:
        query = "SELECT * FROM activity_options"
        results = db.execute_query(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500