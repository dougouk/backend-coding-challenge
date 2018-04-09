"""
"""

import logging
import os
import uuid
import redis

from flask import Flask, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = redis.Redis(host='redis', decode_responses=True)

os.makedirs('/data', exist_ok=True)
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'



@app.route('/suggestions', methods=['GET'])
def upload_wav():
    # Get query parameters
    query_location = request.args.get('q')

    query_lat = request.args.get('latitude')
    query_long = request.args.get('longitude')
