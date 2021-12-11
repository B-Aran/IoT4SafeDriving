#Importamos el cliente de mqtt
import paho.mqtt.client as mqtt
import time
import random
import json

def generate_data():
    latitud = random.uniform(40.330,40.333)
    longitud = random.uniform(-3.765,-3.769)
    altitud = random.uniform(664.8,665.3)
    body = {
        "latitud": latitud,
        "longitud": longitud,
        "altitud": altitud
    }
    return body

#Override customizado del metodo on_connect
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print(f"Connection OK RC = {rc}")
    else:
        print(f"Bad connection RC = {rc}")

def on_publish(client, userdata, mid):
    print(f"Client = {client.name}")
    print(f"Mid = {mid}")

#Metodo para crear ids unicos
def generate_client_id_time():
    return f"VehicleGPS-IoT4SafeDriving-{int(time.time())}"

client_id = generate_client_id_time()
broker_address = "127.0.0.1"
port = 1883

#clean_session=false xra recordar y guardar valores que se ha podido perder por estar offline
client = mqtt.Client(client_id = client_id, clean_session=False)
client.name = client_id #No se puede acceder a client_id, es privado
client.on_connect = on_connect #sincronizamos metodos con callbacks
client.on_publish = on_publish
client.connect(host=broker_address, port=port)
while True:
    client.publish("IoT4SafeDriving-GPS", json.dumps(generate_data()))
    time.sleep(1)
