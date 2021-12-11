import requests
import time
import random

while(True):
    latitud = random.uniform(40.330,40.333)
    longitud = random.uniform(-3.765,-3.769)
    altitud = random.uniform(664.8,665.3)
    body = {
        "latitud": latitud,
        "longitud": [longitud,longitud],
        "altitud": altitud
    }
    print(body)
    r = requests.post('http://localhost:5000/datos_gps', json=body)
    print(r)
    time.sleep(1)
