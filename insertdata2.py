import db
from datetime import datetime
import json


def insert_data(recv_data):
    search_time = datetime.now().strftime('%Y-%m-%d')
    data = json.loads(recv_data[1:-1])
    data2 = json.loads(recv_data)
    print(type(data2[0]))
    check_data = db.db.Sensor.find_one({'date': search_time})
    
    # print(int(data["values"][0]))
    if check_data != None:
        i = 0
        while i < len(data2):
            db.db.Sensor.update({'date': search_time}, {'$push': {'data': {
                                'device_id': data2[i]["device_id"], 'value': int(data2[i]["values"][0])}}})
            i += 1
        return True
    else:
        data["values"] = int(data["values"][0])
        db.db.Sensor.insert_one({'date': search_time, 'data': [data]})
        return False
    return False


def store_request(sent_data):
    search_time = datetime.now().strftime('%Y-%m-%d')
    check_data = db.db.Board.find_one({'date': search_time})
    if check_data != None:
        db.db.Board.update({'date': search_time}, {
            '$push': {'data': sent_data}})
        return True
    else:
        db.db.Board.insert_one({'date': search_time, 'data': [sent_data]})
        return True
    return False
    # db.db.Board.insert_one(sent_data)
