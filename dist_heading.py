import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371.0 
    
    # Convert decimal degrees to radians
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    
    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return r * c


import math

def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the bearing between two points.
    Returns: Bearing in degrees (0-360)
    """
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    diff_lon = math.radians(lon2 - lon1)

    # Formula
    y = math.sin(diff_lon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(diff_lon)
    
    bearing_rad = math.atan2(y, x)
    
    # Convert radians to degrees
    bearing_deg = math.degrees(bearing_rad)
    
    # Normalize to 0-360
    return (bearing_deg + 360) % 360





# --- Example Usage ---
# Coordinates for London
##lat_lon1 = (51.5074, -0.1278)
# Coordinates for Paris
##lat_lon2 = (48.8566, 2.3522)

lat_lon1 = (40.44527, -80.02799)  ## pittsubrgh
##lat_lon2 = (40.60205, -79.92496)      ## home
lat_lon2 = (40.37497, -80.62441)

distance = haversine(lat_lon1[0], lat_lon1[1], lat_lon2[0], lat_lon2[1])

print("Distance: {:.2f} km".format(distance))
print("Distance: {:.2f} miles".format(distance*.621))

heading = calculate_bearing(lat_lon1[0], lat_lon1[1], lat_lon2[0], lat_lon2[1])

print("Heading:", heading, "degrees")

# Output: Distance: 343.46 km
