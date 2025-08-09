from flask import Blueprint, jsonify
from app.services.database import Database

food_bp = Blueprint('food', __name__)
db = Database()

@food_bp.route('/api/food-options', methods=['GET'])
def get_food_options():
    try:
        query = "SELECT * FROM food_options"
        results = db.execute_query(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500
