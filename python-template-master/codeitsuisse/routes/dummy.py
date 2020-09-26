import logging
import json
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/dummy', methods=['POST'])
def getdummy():
    data = request.get_json();
    result = 200
    return json.dumps(result)