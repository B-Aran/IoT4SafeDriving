import requests
import time
import random

while(True):
    yaw = random.uniform(0,3)
    pitch = random.uniform(0,3)
    roll = random.uniform(0,3)
    body = {
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll
    }
    print(body)
    r = requests.post('http://localhost:5000/datos_imu', json=body)
    print(r)
    time.sleep(1)
