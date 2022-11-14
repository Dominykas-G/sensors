#from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'rpi', 'rpi321' 'data')
client.switch_database('data')

json_payload = []

data = {
    "measurement": "device_1",
    "tags": {
        "sensor": "1"
    },
    "time": datetime.now(),
    "fields": {
        "val": 10
    }
}
json_payload.append(data)

client.write_points(json_payload)