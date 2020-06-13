import paho.mqtt.client as mqtt

broker_address = "13.76.250.158"
client = mqtt.Client('P1')
client.username_pw_set(username='BKvm2', password='Hcmut_CSE_2020')
print("Connecting to broker")
client.connect(broker_address, port=1883)
print("Connected")