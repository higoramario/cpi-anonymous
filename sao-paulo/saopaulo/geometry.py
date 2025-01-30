import pandas as pd

# Ref.:
# http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html
def point_in_poly(x, y, poly):
   # check if point is a vertex
   if [x,y] in poly: return True

   # check if point is on a boundary
   for i in range(len(poly)):
      p1 = None
      p2 = None
      if i==0:
         p1 = poly[0]
         p2 = poly[1]
      else:
         p1 = poly[i-1]
         p2 = poly[i]
      if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
         return True
      
   n = len(poly)
   inside = False

   p1 = poly[0]
   p1x = p1[0]
   p1y = p1[1]
   for i in range(n+1):
      p2 = poly[i % n]
      p2x = p2[0]
      p2y = p2[1]
      if y > min(p1y, p2y):
         if y <= max(p1y, p2y):
            if x <= max(p1x, p2x):
               if p1y != p2y:
                  xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
               if p1x == p2x or x <= xints:
                  inside = not inside
      p1x,p1y = p2x,p2y

   return inside


def hexagon_of(station, hexagons):
    for h in hexagons:
        vertices = h['geometry']['coordinates'][0]
        # reversing latitude and longitude
        new_vertices = [ 
            [vertices[0][1], vertices[0][0]],
            [vertices[1][1], vertices[1][0]],
            [vertices[2][1], vertices[2][0]],
            [vertices[3][1], vertices[3][0]],
            [vertices[4][1], vertices[4][0]],
            [vertices[5][1], vertices[5][0]],
        ]
        if point_in_poly(station['latitude'], station['longitude'], new_vertices):
            return h['properties']['hex_id']

def match_stations_and_hexagons(bikestations, hexagons):
    rel_list = []
    for i in range(len(bikestations)):
        hex_id = hexagon_of(bikestations[i], hexagons)
        rel_list.append((bikestations[i]['id'], bikestations[i]['name'], hex_id))
    geographical = pd.DataFrame(rel_list, columns=['station_id', 'station_name', 'hex_id'])
    geographical.set_index('station_id', inplace=False)
    return geographical

def adjacent_hexagons(hex_id):
    def join(x, y):
        return str(x) + 'x' + str(y)
        
    coords = hex_id.split('x')
    x = int(coords[0])
    y = int(coords[1])
    
    if x % 2 == 0:
        return [
            join(x, y+1),
            join(x+1, y+1),
            join(x+1, y),
            join(x, y-1),
            join(x-1, y),
            join(x-1, y+1)
        ]
    else:
        return [
            join(x, y+1),
            join(x+1, y),
            join(x+1, y-1),
            join(x, y-1),
            join(x-1, y-1),
            join(x-1, y)
        ]
