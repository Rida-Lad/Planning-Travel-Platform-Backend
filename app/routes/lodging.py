from flask import Blueprint, jsonify
from app.services.database import Database

lodgings_bp = Blueprint('lodgings', __name__)
db = Database()

@lodgings_bp.route('/api/lodgings-options', methods=['GET'])
def get_activity_options():
    try:
        query = "SELECT * FROM lodging_options"
        results = db.execute_query(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500