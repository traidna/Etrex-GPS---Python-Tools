"""
etrex_funcs - additional functions to use with the etrex GPS interface

distance - calculate the distance between two points given lat and lon
distance(lat1, lon1, lat2, lon2)

bearing - calculate the angle from North to go from point 1 to point2
          given the lat and lon of each point

bearing(lat1, lon1, lat2, lon2)
          
"""

import math

def distance(lat1, lon1, lat2, lon2):
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


def bearing(lat1, lon1, lat2, lon2):
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



