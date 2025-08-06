from flask import Blueprint, request, jsonify
from app.data import city_coords, no_highway_pairs
from app.utils.geo import haversine_distance

bp = Blueprint('cost_calculation_2', __name__, url_prefix='/api')

@bp.route('/calculate-car', methods=['POST'])
def calculate_cost_car():
    data = request.get_json()
    
    # Validation and processing
    start = data.get("start")
    end = data.get("end")
    road_type = data.get("roadType")
    fuel_efficiency = float(data.get("fuelEfficiency"))
    fuel_price = float(data.get("fuelPrice"))

    # Validate cities
    if start not in city_coords or end not in city_coords:
        return jsonify({"error": "Invalid city name"}), 400
    if start == end:
        return jsonify({"error": "Start and end cities cannot be the same"}), 400
    if road_type == "highway" and ((start, end) in no_highway_pairs or (end, start) in no_highway_pairs):
        return jsonify({"error": f"No highway available between {start} and {end}"}), 400

    # Calculate distance
    distance = haversine_distance(city_coords[start], city_coords[end])
    distance *= 1.17  # Adjust for real road distance

    # Calculate costs
    toll_fee = calculate_toll(road_type, distance)
    liters_needed = distance / fuel_efficiency
    total_cost = liters_needed * fuel_price + toll_fee

    return jsonify({
        "distance_km": round(distance, 2),
        "liters_needed": round(liters_needed, 2),
        "estimated_cost": round(total_cost, 2),
        "toll_fee": round(toll_fee, 2)
    })

def calculate_toll(road_type, distance):
    if road_type != "highway":
        return 0
    if distance <= 100: return 30
    elif distance <= 200: return 50
    elif distance <= 350: return 70
    else: return 110