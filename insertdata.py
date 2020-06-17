import db
from datetime import datetime
import json


def insert_data(recv_data):
    search_time = datetime.now().strftime('%Y-%m-%d')
    data = json.loads(recv_data[1:-1])
    check_data = db.db.Sensor.find_one({'date': search_time})

    # print(int(data["values"][0]))
    if check_data != None:
        db.db.Sensor.update({'date': search_time}, {
                            '$push': {'data': {'device_id': 'Light', 'value': int(data["values"][0])}}})
        return True
    else:
        data["values"] = int(data["values"][0])
        db.db.Sensor.insert_one({'date': search_time, 'data': [data]})
        return False
    return False

def store_request(sent_data):
    search_time = datetime.now().strftime('%Y-%m-%d')
    check_data = db.db.Board.find_one({'date': search_time})
    db.db.Board.insert_one(sent_data)
