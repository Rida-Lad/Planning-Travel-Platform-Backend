from math import radians, cos, sin, sqrt, atan2

def haversine_distance(coord1, coord2):
    R = 6371  # Radius of the Earth in km
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km