import db
from datetime import datetime
import json
import app
import connect
import copy

def insert_data(recv_data):
    search_time = datetime.now().strftime('%Y-%m-%d')
    data = json.loads(recv_data[1:-1])
    check_data = db.db.Sensor.find_one({'date': search_time})
    # Auto refine light intensity value
    if app.user_right == False and app.auto_mode == True:
        if int(data["values"][0]) < 10:
            print("Auto-mode")
            store_data = {'device_id': 'LightD', 'values': ['1', '255']}
            send_data = "[" + str(store_data).replace("\'", "\"") + "]"
            connect.client.on_publish = connect.on_publish
            ret = connect.client.publish("Topic/LightD", send_data)
            print("ret is", ret)
            print(store_data)
            print(send_data)
            a, b = ret
            if a == 0:
                store_data['time'] = datetime.now().strftime('%H:%M:%S')
                # insertdata.store_request(store_data)
    # print(int(data["values"][0]))
    if check_data != None:
        db.db.Sensor.update({'date': search_time}, {
                            '$push': {'data': {'device_id': data["device_id"], 'value': int(data["values"][0])}}})
        return True
    else:
        data["values"] = int(data["values"][0])
        db.db.Sensor.insert_one({'date': search_time, 'data': [data]})
        return False
    return False

def store_request(sent_data):
    search_time = datetime.now().strftime('%Y-%m-%d')
    check_data = db.db.Board.find_one({'date': search_time})
    schedule = copy.deepcopy(sent_data['schedule'])
    if schedule['freq'] == 0:
        schedule['date'] = datetime.now().strftime('%Y-%m-%d')
    print(schedule)
    db.db.Board.update({'doc': 'schedule'}, {'$push': {'data': schedule}})
    if check_data != None:
        db.db.Board.update({'date': search_time}, {'$push': {'data': sent_data}})
        return True
    else:
        db.db.Board.insert_one({'date': search_time, 'data': [sent_data]})
        return True
    return False
    # db.db.Board.insert_one(sent_data)
