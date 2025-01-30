import urllib.request as req

prefix = 'https://drive.google.com/uc?export=download&id='

req.urlretrieve(prefix + '1om3ZEnYuUZ5vL358mkFkUP-wc1ZSC6QK', 'bikescience/__init__.py')
req.urlretrieve(prefix + '1G99pY8D19u8932zAhZ6RL34YP29XRjj6', 'bikescience/arrow.py')
req.urlretrieve(prefix + '1CiQhWEUA4D9MBGda4crhilx9fwbghRH0', 'bikescience/charts.py')
req.urlretrieve(prefix + '1_OSbLJSfLkTDopZn_20c0N3gO_iWhrM0', 'bikescience/distributions.py')
req.urlretrieve(prefix + '1elxKgK0afKiS51ItmDZK0oBPkoRuaxlu', 'bikescience/flow.py')
req.urlretrieve(prefix + '1VrLGaUoBouyRNQS40ZNApCNPObIR-YE8', 'bikescience/grid.py')
req.urlretrieve(prefix + '1zH3TzpGeF9CpRUix2Sa-07mROSbn6HPS', 'bikescience/interface.py')
req.urlretrieve(prefix + '1OzoqxFjUb59IXmg8eaOcSnrgxuoVY6-C', 'bikescience/load_trips.py')
req.urlretrieve(prefix + '1dPwWT_JD3ZIbxN76f9nLVKyvsiWYGWO3', 'bikescience/stations.py')
req.urlretrieve(prefix + '1z0_WVzIpHdaNQT6MC2Ypy0d3wfqdmSjO', 'bikescience/tiers.py')


def load_trips():
    from http.cookiejar import CookieJar
    import re
    from bikescience import load_trips as tr
    cj = CookieJar()
    op = req.build_opener(req.HTTPCookieProcessor(cj))
    trips = prefix + '18f4bejSR4sV2nlFoLyjr09r8HUys5bME'
    antivirus_alert = op.open(trips).read()
    confirm_code = re.search(b'confirm=(.+?)&', antivirus_alert).group(1)
    trips += '&confirm=' + confirm_code.decode("utf-8")
    chunk_size = 1024 * 256
    res = op.open(trips)
    with open('trips.csv', 'wb') as w:
        while 1:
            chunk = res.read(chunk_size)
            if not chunk:
                break
            w.write(chunk)
    return tr.load_trips_file('trips.csv')


def load_distances():
    import pandas as pd
    return pd.read_csv(prefix + '1y2sUwAxj-W78FOnNACYAp5G_SDvTv_Hi')


def load_bike_lanes():
    import geopandas as gpd
    req.urlretrieve(prefix + '1ZGXfKNCV7vo2E3EgDKB56XwdQrp1kQ5K', 'BostonBikeFacilities-2018-04t.shx')
    req.urlretrieve(prefix + '1JnPhERz13pcgoGP1Xu6Thra0C8zbMd8_', 'BostonBikeFacilities-2018-04t.shp.xml')
    req.urlretrieve(prefix + '1X-jS990KDg3y3a_hrV-KjESufM-6Ro65', 'BostonBikeFacilities-2018-04t.shp')
    req.urlretrieve(prefix + '1o3HsM09fvlSwxsvql-Zx75Gdw99qw0vm', 'BostonBikeFacilities-2018-04t.sbx')
    req.urlretrieve(prefix + '19HweYSldN8D_KRobwMBLdhrfxnH3tfaS', 'BostonBikeFacilities-2018-04t.sbn')
    req.urlretrieve(prefix + '1eu3P2pw9WoXLNJlCQafUoiV2K9re94x2', 'BostonBikeFacilities-2018-04t.prj')
    req.urlretrieve(prefix + '1sk2ciUvsWJWcMsOHUN3WxfgaZk8URWPz', 'BostonBikeFacilities-2018-04t.dbf')
    req.urlretrieve(prefix + '1d9p8ew22E_IIV7fc3jJapAWNLwbTyTov', 'BostonBikeFacilities-2018-04t.cpg')
    return gpd.read_file('BostonBikeFacilities-2018-04t.shp')


def load_subway_stops():
    import pandas as pd
    import json
    req.urlretrieve(prefix + '1ntPyRiRrGMQ7UH2CdZVFJON8uE_sj_sf', 'subway.json')
    with open('subway.json') as stops_file:
        subway_stops_data = json.load(stops_file)
    return pd.io.json.json_normalize(subway_stops_data)


def load_rail_ferry_stops():
    import pandas as pd
    import json
    req.urlretrieve(prefix + '1LxbLn58Ax3snjNibhDz79d6s9bCZBihc', 'rail_ferry.json')
    with open('rail_ferry.json') as stops_file:
        rail_ferry_stops_data = json.load(stops_file)
    return pd.io.json.json_normalize(rail_ferry_stops_data)


def load_bus_stops():
    import pandas as pd
    import json
    req.urlretrieve(prefix + '1hwEPWt0hgLi5aBfaGDhIJScHm3PmkHDj', 'bus.json')
    with open('bus.json') as stops_file:
        bus_stops_data = json.load(stops_file)
    return pd.io.json.json_normalize(bus_stops_data)
