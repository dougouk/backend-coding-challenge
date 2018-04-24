import math
import sys
import psycopg2
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from city import City

def edge_d(a, b):
    '''
    Compute the edit distance between two words using dynamic programming
    Input: Word a, Word b
    Output: Graph of distances. A 2-dimensional array
    '''
    
    # Create graph nxm
    n = len(a)
    m = len(b)
    graph = []
    
    # Edge Case
    if n == 0:
        return m
    elif m == 0:
        return n
    
    # One extra column / row for initial empty state
    n += 1
    m += 1
    
    for i in range(n):
        graph.append([0] * m)
    
    # Call helper with graph
    return edit_distance_helper(a, b, graph)

def edit_distance_helper(a, b, graph):
    
    # Solve smallest subproblem 
    n = len(a) + 1
    m = len(b) + 1
    
    for i in range(n):
        graph[i][0] = i
    
    for i in range(1, m):
        graph[0][i] = i
        
    # Solve subproblems recursively
    for i in range(1, n):
        for j in range(1, m):
            diff = 1 if a[i-1] != b[j-1] else 0
            graph[i][j] = min(graph[i-1][j] + 1, graph[i][j-1] + 1, graph[i-1][j-1] + diff)
    return graph
    
# edge_d('exponential', 'polynomial')

# edge_d('Calgary', '')
# edge_d('Snow', 'Know')

def lat_long_d(_lat_a, _long_a, _lat_b, _long_b):
    '''
    Returns distance between two points in km
    '''
    lat_a = math.radians(float(_lat_a))
    lat_b = math.radians(float(_lat_b))
    long_a = math.radians(float(_long_a))
    long_b = math.radians(float(_long_b))
    
    # approximate radius of earth in km
    R = 6373.0
    dlon = long_b - long_a
    dlat = lat_b - lat_a

    a = math.sin(dlat / 2)**2 + math.cos(lat_a) * math.cos(lat_b) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def calc_confidence_level(city, query_location):
    '''
    Input: City object variable
    Calculates and stores the confidence level of the city in-place (city variable is updated)
    
    Confidence level is calculated as follows:
    
    -\-\-\-\-\-
    80% weight on edit distance
    20% weight on physical proximity

    If latitude and longitude are not provided, then 100% weight on edit distance

    Edit distance score calculation
    Score = I / (I + D^2)
        I: Inertia
        D: Edit Distance
    Explanation
        When Edit distance is 0 (names are an exact match), the score is a 1.
        A non-linear decrease in score along with edit distance (Yoronto is 
        much more closely matched with Toronto than Yoro).
        
    Physical distance score calculation
    Score = 1 / (1 + physical_d / 100)
        physical_d: physical distance in km
    Explanation
        Assumed that the objective of the data is for Canadian cities. So the 
        physical distance between cities are only significant when in 100s of kms.
        For example, if 2 cities are within 50 km of each other, their score shouldn't differ too much.
    
    Output: Calculate confidence level
    '''
    
    INERTIA = len(query_location) * 2
    confidence_level = 0.0
    if city.physical_distance:
        confidence_level = 0.8 * (INERTIA / (INERTIA + city.edit_distance**2)) + 0.2 * ( 1 / (1 + city.physical_distance / 200))
    else:
        confidence_level = (INERTIA / (INERTIA + city.edit_distance**2))
    city.confidence_level = confidence_level
    return city.confidence_level

EDIT_DISTANCE_THRESHOLD = 3
def search(query, lat=None, long=None):
    '''
    Inputs
        query: name of city
        lat: optional latitude parameter
        longitude: optional longitude parameter
    Output
        Array of cities that may be good results based on the input parameters
    '''
    con = None
    con = connect(database= 'coveo_cities', user='postgres', host = 'localhost', password='password')
    cur = con.cursor()
    # cur.execute('SELECT * FROM cities')
    cur.execute('SELECT * FROM cities WHERE LOWER(cities.name) LIKE \'%' + query.lower() + '%\'')
    rows = cur.fetchall()
    
    similar_cities = []
    for row in rows:
        confidence_graph = edge_d(query.lower(), row[1].lower())
        if query.lower() in row[1].lower() or confidence_graph[-1][-1] < EDIT_DISTANCE_THRESHOLD:
            city = City(row[1], row[4], row[5])
            city.edit_distance = confidence_graph[-1][-1]
            if lat and long:
                city.physical_distance = lat_long_d(lat, long, row[4], row[5])

            calc_confidence_level(city, query)
            similar_cities.append(city)
    cur.close()
    con.close()
    return similar_cities


def rows_in_database():
    con = None
    con = connect(database= 'coveo_cities', user='postgres', host = 'localhost', password='password')
    cur = con.cursor()
    cur.execute('SELECT * FROM cities')
    rows = cur.fetchall()
    return len(rows)