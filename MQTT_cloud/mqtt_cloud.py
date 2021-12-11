#Importamos el cliente de mqtt
import paho.mqtt.client as mqtt
#Import de time para generar ids unicos
import time, requests, json

#Override customizado del metodo on_connect
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print(f"Connection OK RC = {rc}")
    else:
        print(f"Bad connection RC = {rc}")

#Override customizado del metodo on_message
def on_message(client, userdata, message):
    print("-------------------------------")
    print(f"Client = {client.name}")
    print(f"Message = {str(message.payload.decode('utf-8'))}")
    print(f"Topic = {message.topic}")
    print(f"Qos={message.qos}")
    if message.topic == "IoT4SafeDriving-GPS":
        r = requests.post('http://localhost:5000/datos_gps', json=json.loads(str(message.payload.decode('utf-8'))))
    else:
        r = requests.post('http://localhost:5000/datos_imu', json=json.loads(str(message.payload.decode('utf-8'))))

#Metodo para crear ids unicos
def generate_client_id_time():
    return f"Cloud-IoT4SafeDriving-{int(time.time())}"


client_id = generate_client_id_time()
broker_address = "127.0.0.1"
port = 1883

#clean_session=false xra recordar y guardar valores que se ha podido perder por estar offline
client = mqtt.Client(client_id = client_id, clean_session=False)
client.name = client_id #No se puede acceder a client_id, es privado
client.on_connect = on_connect #sincronizamos metodos con callbacks
client.on_message = on_message
client.connect(host=broker_address, port=port)
client.subscribe([("IoT4SafeDriving-GPS", 0) , ("IoT4SafeDriving-IMU", 0)])
client.loop_forever()
