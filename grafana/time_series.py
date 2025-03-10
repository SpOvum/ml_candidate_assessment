import time
import random
from influxdb import InfluxDBClient

def generate_and_send_data():
    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('mydatabase') # Replace name of the database with the database you are gonna use

    while True:
        temperature = random.uniform(20, 30)
        data = [
            {
                "measurement": "temperature",
                "tags": {"location": "office"},
                "fields": {"value": temperature}
            }
        ]
        client.write_points(data)
        print(f"Sent temperature: {temperature:.2f}")
        time.sleep(5)

if __name__ == "__main__":
    generate_and_send_data()
