from flask import Flask, request, jsonify
from math import radians, cos, sin, sqrt, atan2
from cities import city_coords
from nohighwaycities import no_highway_pairs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def haversine_distance(coord1, coord2):
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

@app.route('/api/calculate-moto', methods=['POST'])
def calculate_cost():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    road_type = data.get("roadType")  # "nationalroad" or "highway"
    fuel_efficiency = float(data.get("fuelEfficiency"))  # km per liter
    fuel_price = float(data.get("fuelPrice"))  # price per liter

    if start not in city_coords or end not in city_coords:
        return jsonify({"error": "Invalid city name"}), 400
    
    if start == end:
        return jsonify({"error": "Start and end cities cannot be the same"}), 400
   
    if road_type == "highway":
        if (start, end) in no_highway_pairs or (end, start) in no_highway_pairs:
            return jsonify({
                "error": f"No highway available between {start} and {end}"
            }), 400
    


    distance = haversine_distance(city_coords[start], city_coords[end])
    distance *= 1.17

    toll_fee = 0
    if road_type == "highway":
        # Approximate toll pricing based on distance (MAD)
        if distance <= 100:
            toll_fee = 30
        elif distance <= 200:
            toll_fee = 50
        elif distance <= 350:
            toll_fee = 70
        else:
            toll_fee = 110


    liters_needed = distance  / fuel_efficiency
    total_cost = liters_needed * fuel_price + toll_fee

    return jsonify({
        "distance_km": round(distance, 2),
        "liters_needed": round(liters_needed, 2),
        "estimated_cost": round(total_cost, 2),
        "toll_fee": round(toll_fee, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
