import paho.mqtt.client as mqtt  # import the client1
import time
import threading
import db
from datetime import timedelta, datetime
import insertdata
import json

#######################################
recv_data = 0
save_time = 0
flag_connected = 0

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)
    global recv_data
    global save_time
    save_time += 1
    recv_data = str(message.payload.decode("utf-8")).replace("\n", "").replace(" ", "")
    print("recdata", recv_data)
    print(save_time)
    # Insert data to database
    if save_time == 5:
    # print(threading.active_count())
        save_time = 0
        insertdata.insert_data(recv_data)
        print(a)


def on_publish(client, userdata, mid):
    print("publish message result ", mid)

def on_connect(client, userdata, flags, rc):
    global flag_connected
    flag_connected = 1

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0


########################################
broker_address = "13.76.250.158"
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
client.username_pw_set(username='BKvm2', password='Hcmut_CSE_2020')
client.on_message = on_message  # attach function to callback
print("connecting to broker")
client.connect(broker_address, port=1883, keepalive=500)
client.on_connect = on_connect
client.on_disconnect = on_disconnect  # connect to broker
print("connected")
client.loop_start()  # start the loop
print("Subscribing to topic", "Topic/Light")
client.subscribe("Topic/Light")
time.sleep(1)
client.loop_stop()
# client.disconnect()


# Thread loop getting data every 5 minutes
loop_time = 59


def loop_get_data():
    # client.connect(broker_address, port=1883)  # connect to broker
    client.loop_start()
    client.subscribe("Topic/Light")
    time.sleep(1)
    client.loop_stop()
    threading.Timer(loop_time, loop_get_data).start()

threading.Timer(loop_time, loop_get_data).start()
