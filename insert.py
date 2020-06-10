import db
from datetime import datetime
import random

def insert():
    i = 0
    print(datetime.now().strftime('%Y-%m-%d'))
    # db.db.Sensor.insert({'date':datetime.now().strftime('%Y-%m-%d')})
    while i < 90:
        db.db.Sensor.update({'date':datetime.now().strftime('%Y-%m-%d')},{'$push':{'data':{'device_id':1,'value':random.randint(0, 1023)}}})
        i += 1

if __name__ == '__main__':
    insert()

