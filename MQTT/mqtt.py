import paho.mqtt.client as paho
import sys 
import requests

def onMessage(client, userdata, msg) :

    print(msg.topic + " : " +  msg.payload.decode())
    print ('OnMessage rodou no loop da Client  ')
    json_true = {
        "alarme":"1"
    }
    json_false = {
        "alarme":"0"
    }
    def response_false(id):
        requests.put('http://10.84.8.138:5000/alarme/{}'.format(id), json=json_false)

    def response_true(id):
        requests.put('http://10.84.8.138:5000/alarme/{}'.format(id), json=json_true)

    s = "x" + msg.payload.decode()


    for i in range(1,len(s)):
        if s[i] == '1':
            response_true(i)
        elif s[i] == '0': response_false(i)
            


client = paho.Client()
client.on_message =  onMessage 

print("Rodando")

if client.connect("localhost", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exist(-1)

elif client.connect("localhost", 1883, 60) == 0:
    print("Connected to MQTT Broker!")

client.subscribe("projeto")

try: 
    print("Press CTRL+C to exist... Loop Forever ON!")
    client.loop_forever()
    
except:
    print("Disconnecting from broker")
    client.disconnect()