#from influxdb import InfluxDBClient
from datetime import datetime

#client = InfluxDBClient('localhost', 8086, 'rpi', 'rpi321' 'data')
#client.switch_database('data')


def switch_database(val):
    try:
        device_no = int(val)
    except ValueError:
        print("Can't convert {} into integer".format(val))
    if device_no == 1:
        #client.switch_database("device_1")
        print("Switched to database device_1 \n")
    elif device_no == 2:       
        #client.switch_database("device_2")
        print("Switched to database device_2 \n")
    else:
        print("No database with integer {0}! No device_{0}".format(device_no))

def upload_data(data):
    json_payload = []
    print("Will try to upload the following raw data: {}".format(data))
    switch_database(data[0])
    for num, var in enumerate(data):
        print(num, var)
        if num!=0:
            try:
                data = {
                "measurement": "sens_data",
                "tags": {
                    "sensor": str(num)
                },
                "time": datetime.now(),
                "fields": {
                    "val": round(float(var),1)
                }
            }
            except:
                print("Can't append non-numeric in array location: {} with value: {}".format(num, var))
            
            json_payload.append(data)
    print(json_payload)



#client.write_points(json_payload)
        

input_data = [2,54.00001, 54,67,'m']

upload_data(input_data)


