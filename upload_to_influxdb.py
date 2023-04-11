from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient(host='localhost', port='8086', username='pi', password='rpi321')
client.switch_database('device_1')


def switch_database(val):
    '''
    This function tries to switch databases on influxDB. The first integer in the list identifies the database.
    Example of received data: [1, 34.7, 30.6]. 1 would be the device identifier while 34.7 and 30.6 are the 
    sensor values. Currently, only two devices are going to be tested.
    '''
    try:
        device_no = int(val)
    except:
        print("Can't convert {} into integer".format(val))
    if device_no == 1:
        client.switch_database("device_1")
        print("Switched to database device_1 \n")
    elif device_no == 2:       
        client.switch_database("device_2")
        print("Switched to database device_2 \n")
    else:
        print("No database with integer {0}! No device_{0}. Aborting upload.".format(device_no))
        return False

def upload_data(data_raw):
    '''
    This function creates json file and tries to upload it to influxDB. First integer of the received data 
    must be device identifier while the following data are the sensor values. Example of received data: 
    1,34.7,30.6. 1 would be the device identifier while 34.7 and 30.6 are the sensor values.
    '''
    json_payload = []
    data = []
    print("Will try to upload the following raw data: {}".format(data))
    
    # putting data into a list
    data = [letter for letter in data_raw.split(",")]

    # if switching database fails - abort
    if switch_database(data[0]) is False:
        return 0
    
    # try to construct json file and upload it
    for num, var in enumerate(data):
        if num!=0:
            try:
                data = {
                "measurement": "sens_data",
                "tags": {
                    "sensor": str(num)
                },
                "time": datetime.now(),
                "fields": {
                    "val": round(float(var), 1)
                }
            }
                json_payload.append(data)

            except:
                print("Can't append non-numeric in array location: {} with value: {}".format(num, var))
                
    # if the list is not empty, try to upload it to influxDB
    if json_payload:
        try:
            print("Uploading json file...")
            client.write_points(json_payload)
        except:
            print("Failed to upload json file.")
    else:
        print("Failed to upload json file because it is empty!")
    
    print(json_payload)

def main():

    # upload_data("1,-9.9,97.887")

if __name__ == "__main__":
    main()
