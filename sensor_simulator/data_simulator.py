import requests, time, random, json

while(True):
    vehicle = random.randint(1,5)
    lat = random.uniform(40.330,40.333)
    lon = random.uniform(-3.765,-3.769)
    alt = random.uniform(664.8,665.3)
    yaw = random.uniform(0,3)
    pit = random.uniform(0,3)
    rol = random.uniform(0,3)

    geojson = {
        "lon": lon,
        "lat": lat,
        "yaw": yaw,
        "pit": pit,
        "rol": rol,
        "alt": alt,
        "veh": vehicle
    }

    print(geojson)
    r = requests.post('http://localhost:5000/datos', json = geojson)
    print(r)
    time.sleep(1)
