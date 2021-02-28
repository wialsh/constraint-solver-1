# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:33:53 2019

@author: wialsh
"""
from typing import List, Dict
import numpy as np
from numpy import radians, degrees, newaxis
from numpy import cos, sin, arcsin, sqrt, arctan2

# np.set_printoptions(suppress=True,precision=15)

## https://en.wikipedia.org/wiki/Earth_radius
# WGS-84 ellipsoid, Mean radius of semi-axes (R1)
r = 6371008.7714  # unit metres

def calculate_the_center_point(coords):
    # type: (List[List[float, float]]) -> List[np.ndarray, np.ndarray]
    """
    https://stackoverflow.com/questions/6671183/calculate-the-center-point-of-multiple-latitude-longitude-coordinate-pairs
    a much earlier question: https://stackoverflow.com/questions/491738/how-do-you-calculate-the-average-of-a-set-of-circular-output/491784#491784
    :param coords: [(lng0, lat0), (lng1, lat1), ...]
    :return: (centre_lat, centre_lng)
    """
    lon_lat = np.array(coords)

    assert lon_lat.shape != (0,)

    nums = lon_lat.shape[0]

    lng_rads, lat_rads = radians(lon_lat).T
    
    x = (cos(lat_rads) * cos(lng_rads)).sum() / nums
    y = (cos(lat_rads) * sin(lng_rads)).sum() / nums
    z = sin(lat_rads).sum() / nums

    #np.arctan2/np.arctan get the same of the output result.
    #but input: np.arctan(y/x) \ np.arctan2(y,x), so the input x elem for np.arctan must unequal 0.
    centre_lng = arctan2(y, x)
    centre_square_root = sqrt(x * x + y * y)
    centre_lat = arctan2(z, centre_square_root)

    return [degrees(centre_lng), degrees(centre_lat)]

def haversine(p0, p1):
    # type: (List[List[float, float]], List[List[float, float]]) -> np.ndarray
    """
    Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
    :param p0: [[lng, lat], ...]
    :param p1: [[lng, lat], ...]
    :return:
    """
    rad0 = radians(p0)
    rad1 = radians(p1)

    lng0, lat0 = rad0.T
    lng1, lat1 = rad1.T

    dlng = lng1 - lng0
    dlat = lat1 - lat0

    a = sin(dlat / 2) ** 2 + cos(lat0) * cos(lat1) * sin(dlng / 2) ** 2
    c = 2 * arcsin(sqrt(a))
    return c * r



def haversine_matrix(coordinate):
    #type: (List[List[float]]) -> np.ndarray
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    :param coordinate: `list` or `numpy.ndarray`, [[lng, lat], ...]
        e.g. coordinate = ﻿[
                            [100.58556, 13.734766],
                            [100.585709, 13.734672],
                            [100.572233, 13.775265],
                            [100.574075, 13.789008],
                            [100.585628, 13.734734]
                        ]
    :return: n * n distance matrix.
    """
    rads = radians(coordinate)

    n = rads.shape[0]

    lngs, lats = rads.T

    lat0, lng0 = lats, lngs
    lat1, lng1 = lats[:, newaxis], lngs[:, newaxis]

    dlng = (lng1 - lng0).ravel()
    dlat = (lat1 - lat0).ravel()

    a = sin(dlat / 2) ** 2 + (cos(lat0) * cos(lat1)).ravel() * sin(dlng / 2) ** 2
    c = 2 * arcsin(sqrt(a))
    return (c * r).reshape((n, n))

def haversine_matrix_new(coords0, coords1):
    #type: (List[List[float]], List[List[float]]) -> np.ndarray
    """
    the shape of the input data can diff.
    :param coords0: `list` or `numpy.ndarray`, [[lng, lat], ...], the shape of matrix is (n,2).
    :param coords1: `list` or `numpy.ndarray`, [[lng, lat], ...], the shape of matrix is (m,2).
    :return: n * m distance matrix.
    """
    rads0 = radians(coords0)
    rads1 = radians(coords1)
    n = rads0.shape[0]
    m = rads1.shape[0]

    lng0, lat0 = rads0.T

    lng1, lat1 = rads1.T
    lng1, lat1 = lng1[:, newaxis], lat1[:, newaxis]

    dlng = (lng1 - lng0).ravel()
    dlat = (lat1 - lat0).ravel()

    a = sin(dlat / 2) ** 2 + (cos(lat0) * cos(lat1)).ravel() * sin(dlng / 2) ** 2
    c = 2 * arcsin(sqrt(a))
    return (c * r).reshape((m, n)).T

def calculate_polygon_area(geojson):
    #type: (Dict[str, List[List[List[float]]]]) -> float
    """
    Area of a polygon (Coordinate Geometry)
        https://www.mathopenref.com/coordpolygonarea.html
    :param geojson: polygon geojson object
    :return: polygon area
    """
    poly_area = 0
    # TODO: polygon holes at coordinates[1]
    coordinates = geojson['coordinates'][0]
    j = len(coordinates) - 1
    count = len(coordinates)

    for i in range(0, count):
        p1_x = coordinates[i][1]
        p1_y = coordinates[i][0]
        p2_x = coordinates[j][1]
        p2_y = coordinates[j][0]

        poly_area += p1_x * p2_y
        poly_area -= p1_y * p2_x
        j = i

    poly_area /= 2
    return poly_area

def calculate_polygon_area_metres(geojson):
    #type: (Dict[str, List[List[List[float]]]]) -> float
    """
    Area of a polygon (Coordinate Geometry)
        https://www.mathopenref.com/coordpolygonarea.html
        https://stackoverflow.com/questions/2861272/polygon-area-calculation-using-latitude-and-longitude-generated-from-cartesian-s
    :param geojson: polygon geojson object
    :return: polygon area
    """
    poly_area = 0
    # TODO: polygon holes at coordinates[1]
    coordinates = geojson['coordinates']

    for coordinate in coordinates:
        coordinate = coordinate[0]
        count = len(coordinate)
        for i in range(count - 1):
            c0 = coordinate[i]
            c1 = coordinate[i+1]
            #c0 = (lng, lat)
            poly_area += radians(c1[0] - c0[0]) * (2 + sin(radians(c0[1])) + sin(radians(c1[1])))
    poly_area = poly_area * r * r / 2
    return abs(poly_area)