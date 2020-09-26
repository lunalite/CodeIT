import logging
import json
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def find_lowest_cost():
    map = request.get_json()
    maps = map.get("salad_prices_street_map")
    n = map.get("number_of_salads")
    possible_stores =[]
    possible_cost = []
    for street in maps:
        ls_nox = ' '.join(street).split('X')
        for part in ls_nox:
            part = part.strip()
            if part =='':
                continue
            str_digits = part.split(' ')
            for i in range(len(str_digits)):
                str_digits[i] = int(str_digits[i]) 
            
            if len(str_digits)>=n:
                for index in range(len(str_digits) - n+1):
                    possible_stores.append(str_digits[index:index+n])
                    possible_cost.append(sum(str_digits[index:index+n]))
    if len(possible_cost) == 0:
        ans = 0
    else:
        ans = min(possible_cost)

    return json.dumps({"result": ans })