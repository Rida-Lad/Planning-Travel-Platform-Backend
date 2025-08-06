from flask import Blueprint, request, jsonify
from app.services.database import Database

travel_bp = Blueprint('travel', __name__)
db = Database()

@travel_bp.route('/api/bus-options', methods=['GET'])
def get_travel_options():
    end_city = request.args.get('end_city')

    if not end_city:
        return jsonify({'error': 'Missing end_city parameter'}), 400

    try:
        query = "SELECT * FROM bus_travel_options WHERE end_city = %s"
        results = db.execute_query(query, (end_city,))
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500
