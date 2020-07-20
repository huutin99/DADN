import schedule 
import time
import app
import connect
import db
import copy

def send_publish(data):
    app.auto_mode = False
    print("On schedule, auto:", app.auto_mode)
    while data['schedule']['duration'] > 0:
        connect.client.on_publish = connect.on_publish
        sent_data = copy.deepcopy(data)
        sent_data.pop('schedule')
        sent_data = "[" + str(sent_data).replace("\'", "\"") + "]"
        ret = connect.client.publish("Topic/LightD", sent_data)
        print("data", sent_data)
        print("ret on schedule is", ret)
        time.sleep(60)
        data['schedule']['duration'] -= 1
        print("Time left", data['schedule']['duration'])
    app.auto_mode = True
    if data['schedule']['freq'] == 0:
        return schedule.CancelJob
    return True

def make_schedule(data):
    # print(data['schedule']['start'], type(data['schedule']['start']))
    schedule.every().day.at(data['schedule']['start']).do(send_publish, data = data)
    app.stop_threads = False
    while True:
        schedule.run_pending()
        # print("Rerun schedule, schedule list:", schedule.jobs)
        time.sleep(5)
        if app.stop_threads: 
            print("Stoped old schedule")
            break