import paho.mqtt.client as mqtt #import the client1
import time
import threading
import db
from datetime import timedelta, datetime
import insertdata

#######################################
recv_data = 0
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    global recv_data 
    recv_data = str(message.payload.decode("utf-8"))
    # Insert data to database
    insertdata.insert_data(recv_data)

########################################
broker_address="13.76.250.158"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.username_pw_set(username='BKvm2', password='Hcmut_CSE_2020')
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address, port=1883) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","Topic/Light")
client.subscribe("Topic/Light")
print("Publishing message to topic","Topic/LightD")
client.publish("Topic/LightD","OFF")
client.loop_stop()

# Thread loop getting data every 5 minutes
def loop_get_data():
        client.loop_start()
        client.subscribe("Topic/Light")
        client.loop_stop()
        threading.Timer(3000, loop_get_data).start()
threading.Timer(3000, loop_get_data).start()
