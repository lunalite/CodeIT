## revisitgeometry.py

import logging
import json
from flask import request, jsonify
from codeitsuisse import app
import numpy as np
import shapely
import shapely.geometry


logger = logging.getLogger(__name__)


@app.route('/revisitgeometry', methods=['POST'])
def get_intercepts():
    geo = request.get_json()
    cord_list = []
    for point in geo.get('shapeCoordinates'):
        # print(point['x'], point['y'])
        cord_list.append([point['x'], point['y']])

    polygon = shapely.geometry.Polygon(cord_list)

    line_lis = []
    for point in geo.get('lineCoordinates'):
        # print(point['x'], point['y'])
        line_lis.append([point['x'], point['y']])
    line = shapely.geometry.LineString(line_lis)
    ring = shapely.geometry.LineString(list(polygon.exterior.coords))

    minx, miny, maxx, maxy = polygon.bounds
    bounding_box = shapely.geometry.box(minx, miny, maxx, maxy)
    a, b = line.boundary
    if a.x == b.x:  # vertical line
        extended_line = shapely.geometry.LineString([(a.x, miny), (a.x, maxy)])
    elif a.y == b.y:  # horizonthal line
        extended_line = shapely.geometry.LineString([(minx, a.y), (maxx, a.y)])
    else:
        # linear equation: y = k*x + m
        k = (b.y - a.y) / (b.x - a.x)
        m = a.y - k * a.x
        y0 = k * minx + m
        y1 = k * maxx + m
        x0 = (miny - m) / k
        x1 = (maxy - m) / k
        points_on_boundary_lines = [shapely.geometry.Point(minx, y0), shapely.geometry.Point(maxx, y1),
                                    shapely.geometry.Point(x0, miny), shapely.geometry.Point(x1, maxy)]
        points_sorted_by_distance = sorted(points_on_boundary_lines, key=bounding_box.distance)
        extended_line = shapely.geometry.LineString(points_sorted_by_distance[:2])

    try:
        point_list = list(ring.intersection(extended_line))
    except:
        point_list = ring.intersection(extended_line).coords

    result = []
    for pair in point_list:
        coords = pair.coords[0]
        result.append({"x": round(coords[0], 2), 'y': round(coords[1], 2)})
    print(result)
    return json.dumps(result)
