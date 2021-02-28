# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:40:05 2019

@author: wialsh
"""
from typing import Tuple, List
import numpy as np

## verification: http://www.gpsspg.com/maps.htm
x_pi = np.pi * 3000.0 / 180.0
a = 6378245.0  # semi-major axis
ee = 0.00669342162296594323  # flattening


def gcj02tobd09(lon, lat):
    # type: (float, float) -> List[float, float]
    z = np.sqrt(lon * lon + lat * lat) + 0.00002 * np.sin(lat * x_pi)

    theta  = np.arctan2(lat, lon) + 0.000003 * np.cos(lon * x_pi)

    bd_lon = z * np.cos(theta) + 0.0065
    bd_lat = z * np.sin(theta) + 0.006
    return [bd_lon, bd_lat]


def bd09togcj02(bd_lon, bd_lat):
    # type: (float, float) -> List[float, float]
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = np.sqrt(x * x + y * y) - 0.00002 * np.sin(y * x_pi)

    theta = np.arctan2(y, x) - 0.000003 * np.cos(x * x_pi)

    gg_lon = z * np.cos(theta)
    gg_lat = z * np.sin(theta)

    return [gg_lon, gg_lat]


def wgs84togcj02(lon, lat):
    # type: (float, float) -> List[float, float]
    if out_of_china(lon, lat):
        return [lon, lat]

    dlat = transform_lat(lon - 105.0, lat - 35.0)
    dlon = transform_lon(lon - 105.0, lat - 35.0)

    radlat = lat / 180.0 * np.pi

    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic

    sqrtmagic = np.sqrt(magic)

    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * np.pi)
    dlon = (dlon * 180.0) / (a / sqrtmagic * np.cos(radlat) * np.pi)

    mglat = lat + dlat
    mglon = lon + dlon

    return [mglon, mglat]


def gcj02towgs84(lon, lat):
    # type: (float, float) -> List[float, float]
    if out_of_china(lon, lat):
        return [lon, lat]

    dlat = transform_lat(lon - 105.0, lat - 35.0)
    dlon = transform_lon(lon - 105.0, lat - 35.0)

    radlat = lat / 180.0 * np.pi

    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic

    sqrtmagic = np.sqrt(magic)

    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * np.pi)
    dlon = (dlon * 180.0) / (a / sqrtmagic * np.cos(radlat) * np.pi)

    mglat = lat + dlat
    mglon = lon + dlon

    return [lon * 2 - mglon, lat * 2 - mglat]

def lonlat2mercator(lon, lat):
    # type: (float, float) -> Tuple[float, float]
    """ arbitrary CSYS input. """
    x = lon * 20037508.34 / 180.0
    y = np.log(np.tan((90.0 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    y *= 20037508.34 / 180.0
    return x, y

def transform_lat(lon, lat):
    # type: (float, float) -> float
    ret = -100.0 + 2.0 * lon + 3.0 * lat + 0.2 * lat * lat + 0.1 * lon * lat + 0.2 * np.sqrt(np.fabs(lon))

    ret += (20.0 * np.sin(6.0 * lon * np.pi) + 20.0 * np.sin(2.0 * lon * np.pi)) * 2.0 / 3.0
    ret += (20.0 * np.sin(lat * np.pi) + 40.0 * np.sin(lat / 3.0 * np.pi)) * 2.0 / 3.0
    ret += (160.0 * np.sin(lat / 12.0 * np.pi) + 320 * np.sin(lat * np.pi / 30.0)) * 2.0 / 3.0
    return ret


def transform_lon(lon, lat):
    # type: (float, float) -> float
    ret = 300.0 + lon + 2.0 * lat + 0.1 * lon * lon + 0.1 * lon * lat + 0.1 * np.sqrt(np.fabs(lon))

    ret += (20.0 * np.sin(6.0 * lon * np.pi) + 20.0 * np.sin(2.0 * lon * np.pi)) * 2.0 / 3.0
    ret += (20.0 * np.sin(lon * np.pi) + 40.0 * np.sin(lon / 3.0 * np.pi)) * 2.0 / 3.0
    ret += (150.0 * np.sin(lon / 12.0 * np.pi) + 300.0 * np.sin(lon / 30.0 * np.pi)) * 2.0 / 3.0
    return ret


def out_of_china(lon, lat):
    #type: (float, float) -> bool
    res = False
    if lon < 72.004 or lon > 137.8347:
        res = True
    elif lat < 0.8293 or lat > 55.8271:
        res = True
    return res


if __name__ == '__main__':
    lon = 113.332656

    lat = 23.152902
    lon, lat = bd09togcj02(lon, lat)
    print(lon, lat)
    lon, lat = gcj02towgs84(lon, lat)
    print(lon, lat)

    result1 = gcj02tobd09(lon, lat)

    result2 = bd09togcj02(lon, lat)

    result3 = wgs84togcj02(lon, lat)

    result4 = gcj02towgs84(lon, lat)

    print(result1, result2, result3, result4)

    lon, lat = wgs84togcj02(lon, lat)
    print(gcj02tobd09(lon, lat))
