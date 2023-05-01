from influxdb import InfluxDBClient
from datetime import datetime
import passwords

client = InfluxDBClient(host='localhost', port='8086', username=passwords.influx_username, password=passwords.influx_pasword, database='device_1')

def construct_json(data):
    json_payload = []
    for num, var in enumerate(data):
        if num!=0:
            json_data = {
            "measurement": "sens_data",
            "tags": {
                "sensor": str(num)
            },
            "time": datetime.utcnow().isoformat() + "Z",
            "fields": {
                "val": round(float(var), 1)
            }
        }
            json_payload.append(json_data)
    return json_payload


def upload_data(data_raw):
    '''
    This function creates json file and tries to upload it to influxDB. First integer of the received data 
    must be device identifier while the following data are the sensor values. Example of received data: 
    1,34.7,30.6. 1 would be the device identifier while 34.7 and 30.6 are the sensor values.
    '''
    data = [letter for letter in data_raw.split(",")]
    
    try:
        client.switch_database('device_{}'.format(data[0]))
        json_payload = construct_json(data)
    except Exception as e:
        print(e)

    # if the list is not empty, try to upload it to influxDB
    if json_payload:
        try:
            print('Uploading json file...')
            client.write_points(json_payload)
            print('The uploaded data in device_{} has a:'.format(int(data[0])))
            for data_point in json_payload:
                print('tag: {} \nfield {} \ntime: {}'.format(data_point['tags'], data_point['fields'], data_point['time']))
            print('\n')
        except Exception as e:
            print(e)
    else:
        print("Failed to upload json file because it is empty!")

def main():
    
    # used to debug
    upload_data(r"\x1cmY<yz]8,kjhhj")
    
if __name__ == "__main__":
    main()
