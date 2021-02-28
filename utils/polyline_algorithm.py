# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:58:58 2019

@author: wialsh

E-mail: hebiyaozizhou@gmail.com
"""
from typing import List, Dict
# https://github.com/valhalla/valhalla-docs/blob/master/decoding.md

precs = 1e6
# six degrees of precision in valhalla
inv = 1.0 / precs

def encode(points):
    # type: (List[Dict[str, float]]) -> str
    """

    :param points: [{"lat": -44.395503, "lng": 169.994841}, ...] or [[lng, lat], ...]
    :return:
    """
    input_is_list = isinstance(points[0], list)

    output = ''

    #handy lambda to turn an integer into an encoded string
    def serialize(number):
        chars = ''
        #move the bits left 1 position and flip all the bits if it was a negative number
        number = ~(number << 1) if number < 0 else (number << 1)
        #write 5 bit chunks of the number
        while (number >= 0x20):
            nextValue = (0x20 | (number & 0x1f)) + 63
            chars += chr(nextValue)
            number >>= 5

        #write the last chunk
        number += 63
        chars += chr(number)
        return chars

    #this is an offset encoding so we remember the last point we saw
    last_lon, last_lat = 0, 0
    #for each point
    for ll in points:
        #shift the decimal point 5 places to the right and truncate
        lon = int((ll[0] if input_is_list else ll['lng']) * precs)
        lat = int((ll[1] if input_is_list else ll['lat']) * precs)
        #encode each coordinate, lat first for some reason
        output += serialize(lat - last_lat)
        output += serialize(lon - last_lon)
        #remember the last one we encountered
        last_lon = lon
        last_lat = lat
    return output



# decode an encoded string
def decode(encoded):
    # type: (str) -> List[List[float]]
    decoded = []
    previous = [0, 0]
    i = 0

    # for each byte
    while i < len(encoded):

        # for each coord (lat, lon)
        ll = [0, 0]
        for j in [0, 1]:
            shift = 0
            byte = 0x20

            # keep decoding bytes until you have this coord
            while byte >= 0x20:
                byte = ord(encoded[i]) - 63
                i += 1
                ll[j] |= (byte & 0x1f) << shift
                shift += 5

            # get the final value adding the previous offset and remember it for the next
            ll[j] = previous[j] + (~(ll[j] >> 1) if ll[j] & 1 else (ll[j] >> 1))
            previous[j] = ll[j]

        # scale by the precision and chop off long coords also flip the positions so
        # its the far more standard lon,lat instead of lat,lon
        decoded.append([float('%.6f' % (ll[1] * inv)), float('%.6f' % (ll[0] * inv))])

    # result = {
    #     'lng': list(map(lambda x: x[0], decoded)),
    #     'lat': list(map(lambda x: x[1], decoded))
    # }
    # # hand back the list of coordinates
    # #shape: {"lng": [lng0, lng1, ...], "lat": [lat0, lat1, ...]}
    # route_shape_horizontal = result

    #shape: [[lng0, lat0], [lng1, lat1], ...]
    route_shape_vertical = decoded
    # return route_shape_vertical, route_shape_horizontal
    return route_shape_vertical

def verification(points):
    encoded = encode(points)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)

    input_is_list = isinstance(points[0], list)
    for i, ll in enumerate(decoded):
        lon = int(ll[0] * precs)
        lat = int(ll[1] * precs)

        lon_origin = int((points[i][0] if input_is_list else points[i]['lng']) * precs)
        lat_origin = int((points[i][1] if input_is_list else points[i]['lat']) * precs)
        if (lon != lon_origin) | (lat != lat_origin):
            return False
    return True



if __name__ == '__main__':
    points = [{"lat": -44.39550305255167, "lng": 169.9948411995265},
              {"lat": -44.46149536878286, "lng": 169.9792634324822},
              {"lat": -44.46292423181652, "lng": 169.9819261954818},
              {"lat": -44.5036713034329, "lng": 170.0260870905314},
              {"lat": -44.5036713034329, "lng": 170.0260870905314},
              {"lat": -44.54993815165437, "lng": 170.0886754320656},
              {"lat": -44.55196573403156, "lng": 170.0888672938292},
              {"lat": -44.59632393908183, "lng": 170.1672103443836},
              {"lat": -44.62121982597245, "lng": 170.2550457326418},
              {"lat": -44.6470204554914, "lng": 170.3347002995855},
              {"lat": -44.68112738341529, "lng": 170.3940738459773},
              {"lat": -44.68112738341529, "lng": 170.3940738459773},
              {"lat": -44.72374600828134, "lng": 170.464877458448},
              {"lat": -44.73246515086986, "lng": 170.4697679176869},
              {"lat": -44.73261816217322, "lng": 170.4699271473218},
              {"lat": -44.73895333711499, "lng": 170.4739902635761},
              {"lat": -44.84241074886624, "lng": 170.6387768035481},
              {"lat": -44.85430056558641, "lng": 170.6828668551577},
              {"lat": -44.87051250417239, "lng": 170.7299313416432},
              {"lat": -44.85434955920284, "lng": 170.6830330543193},
              {"lat": -44.91906974934499, "lng": 170.8576049936664},
              {"lat": -44.95314650241747, "lng": 170.9140908905965},
              {"lat": -44.95362062477037, "lng": 170.9143049644035},
              {"lat": -44.97142286509738, "lng": 170.9442850203914},
              {"lat": -45.03504637167327, "lng": 170.9195041751218},
              {"lat": -45.07707237046172, "lng": 170.9182191983543},
              {"lat": -45.08135284407467, "lng": 170.9187558962851},
              {"lat": -45.12052439157397, "lng": 170.8943154664439},
              {"lat": -45.17049159858857, "lng": 170.8339692840081},
              {"lat": -45.08137008465346, "lng": 170.9187624916995},
              {"lat": -45.24157269396376, "lng": 170.7828447876226},
              {"lat": -45.3082308685829, "lng": 170.8151689266514},
              {"lat": -45.31026440211135, "lng": 170.8161045985024},
              {"lat": -45.31026440211135, "lng": 170.8161045985024},
              {"lat": -45.40437771011647, "lng": 170.834521483789},
              {"lat": -45.40431325328108, "lng": 170.8345620522004},
              {"lat": -45.49814417496835, "lng": 170.6993048732827},
              {"lat": -45.57065107398254, "lng": 170.6925537531922},
              {"lat": -45.83145348825104, "lng": 170.5057139230617},
              {"lat": -45.83284169905431, "lng": 170.5047213380882},
              {"lat": -45.85074488055441, "lng": 170.5090146072038},
              {"lat": -45.85678432718039, "lng": 170.5132430889644},
              {"lat": -45.85866522202237, "lng": 170.5122949568263},
              {"lat": -45.86449377708683, "lng": 170.5093076640465},
              {"lat": -45.86592079610178, "lng": 170.5081440882483},
              {"lat": -45.86799271217539, "lng": 170.5070841674242},
              {"lat": -45.86795267125516, "lng": 170.5070802705866},
              {"lat": -45.86995102628246, "lng": 170.5044615533606},
              {"lat": -45.87185299876215, "lng": 170.5013165169684},
              {"lat": -45.8719955998755, "lng": 170.5013075799361},
              {"lat": -45.87184831227629, "lng": 170.5013534784244},
              {"lat": -45.87466667828366, "lng": 170.5018430895788},
              {"lat": -45.87540132878888, "lng": 170.502762161555},
              {"lat": -45.87595164301652, "lng": 170.5026205879162},
              {"lat": -45.87745092346409, "lng": 170.5016440580659},
              {"lat": -45.87823003787549, "lng": 170.5014304844617},
              {"lat": -45.88068498912999, "lng": 170.4998968558322},
              {"lat": -45.88250937718987, "lng": 170.49952220076},
              {"lat": -45.89198080361438, "lng": 170.4973435030975},
              {"lat": -45.89313777520309, "lng": 170.4986730099997},
              {"lat": -45.89224012347859, "lng": 170.4996939597901}]

    encoded = encode(points)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)

    print(verification(points))


    points = [
	[-115.1722053039234, 36.11955221409178],
	[-115.1721313078572, 36.11877300592508],
	[-115.1718530355559, 36.11893568847024],
	[-115.1707093194468, 36.11910033468673],
	[-115.1707551475009, 36.11908843720018],
	[-115.1699201278123, 36.11938172169028],
	[-115.1699111355126, 36.11946984721608],
	[-115.1699093428803, 36.11946683752327],
	[-115.1690099471909, 36.11972971659073],
	[-115.1694853283808, 36.11976649160206],
	[-115.1682263280594, 36.11802810318864],
	[-115.1688569517961, 36.11991965664756],
	[-115.1688569517961, 36.11991965664756],
	[-115.1675285964641, 36.12019731104746],
	[-115.1674947150025, 36.12020315668611],
	[-115.1656911951114, 36.11945242772071],
	[-115.1638064433466, 36.11830571915127],
	[-115.1636992680776, 36.11786191282127],
	[-115.1639489446473, 36.11626039534701],
	[-115.1641268954712, 36.11498226436336],
	[-115.1644920689209, 36.11486061902072],
	[-115.1643750175939, 36.11482908729195],
	[-115.1651975771594, 36.11473366344205],
	[-115.1659575649801, 36.11469847725616],
	[-115.1659163836944, 36.11470640174512],
	[-115.1682134136209, 36.11470009188629],
	[-115.168370624137, 36.11469948501724],
	[-115.1720823605617, 36.11457868649419],
	[-115.1724248339435, 36.1145916436199],
	[-115.1724749134095, 36.11464797094256],
	[-115.1721987204342, 36.11457657576251],
	[-115.173114957981, 36.112002682051],
	[-115.1731463943878, 36.11184796751212],
	[-115.1728586376679, 36.11169255213365],
	[-115.17300632738, 36.11059000023432],
	[-115.1729975392109, 36.10932899135754],
	[-115.1730144007331, 36.10983674532654],
	[-115.1731668203578, 36.10958833444774],
	[-115.1730674554599, 36.11093875599695],
	[-115.1729685970813, 36.11075409189559],
	[-115.1728173106321, 36.11129167885137],
	[-115.1724629005301, 36.11155861454359],
	[-115.1721995613275, 36.11161415319872],
	[-115.1703548602955, 36.11105672913137],
	[-115.1679142964463, 36.10832250436106],
	[-115.1672349663044, 36.10791415384843],
	[-115.1685656975609, 36.10833291009894],
	[-115.169458050025, 36.10821211304452],
	[-115.1689992567839, 36.10815676892791],
	[-115.1682257296534, 36.10800759050209],
	[-115.1674879479403, 36.1083527674955],
	[-115.1680141929332, 36.10798511533527],
	[-115.1690957744484, 36.11069501564321],
	[-115.1698706145436, 36.11100670299042],
	[-115.1699685383951, 36.11029103250459],
	[-115.1698029697499, 36.10936988906643],
	[-115.1702179468788, 36.10902545354353]
]

    encoded = encode(points)
    print(encoded)
    decoded = decode(encoded)
    print(decoded)

    print(verification(points))
