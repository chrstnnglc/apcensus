import math

#Computes for the latitude distance        
def LatCoordDistance(lat,offset):
    R = float(6378137)
    rad_lat_offset = offset/R
    new_lat = (lat - rad_lat_offset * 180/math.pi);
    return round(new_lat,6)


#Computes for the longitude distance
def LngCoordDistance(lat,lng,offset):
    R = float(6378137)
    rad_lng_offset =  offset/(R*math.cos(math.pi/180*lat))
    new_lng = (lng + rad_lng_offset * 180/math.pi)
    return round(new_lng,6);
