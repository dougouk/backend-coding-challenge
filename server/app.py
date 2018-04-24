"""
Dongoug Kim
Coveo Backend Coding Challenge
"""

import logging
import os
import uuid
import redis
import algorithm
import json

from flask import Flask, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

# Set up logger and flask app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# r = redis.Redis(host='redis', decode_responses=True)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/readall')
def read_all():
    result = dict()
    result['rows'] = algorithm.goThroughDatabase()
    return json.dumps(result)

@app.route('/suggestions', methods=['GET'])
def upload_wav():
    # Get query parameters
    query_location = request.args.get('q')
    response = dict()

    if query_location is None:
        logger.error('Location query is None')        
        response['error'] = 'Location query must not be empty'
        return json.dumps(response)
    else:
        query_lat = request.args.get('latitude')
        query_long = request.args.get('longitude')

        logger.info(f'Received {query_location} query')

        if query_lat:
            logger.info(f'Additional location info: [{query_lat}:{query_long}]')

        results = algorithm.search(query_location, query_lat, query_long)
        sorted_results = sorted(results, key=lambda x: x.confidence_level, reverse=True)
        sorted_results

        logger.info(f'Results: {sorted_results}')
    

        '''
        TODO
        Wrap up the results into a json response.
        O(n) operation. Is there a better way to encode it to a json response?
        '''
        response['suggestions'] = [ 
            { 
                'name': result.name,
                'latitude': result.lat,
                'longitude': result.long,
                'score': result.confidence_level
            } for result in sorted_results 
        ]
        result = {
            'q': query_location,
            'lat': query_lat,
            'lng': query_long,
            'results': [result.toJSON() for result in sorted_results]
        }
        
        return json.dumps(response)