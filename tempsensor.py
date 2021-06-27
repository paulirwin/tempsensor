import Adafruit_DHT
from Adafruit_IO import Client
import time
import logging
import os

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
DELAY = 60
ADAFRUIT_IO_USERNAME = os.environ["ADAFRUIT_IO_USERNAME"]
ADAFRUIT_IO_KEY = os.environ["ADAFRUIT_IO_KEY"]
TEMP_FEED_NAME = "temp"
HUMIDITY_FEED_NAME = "humidity"
SENSOR_FAILURES_FEED_NAME = "sensorfailures"
API_FAILURES_FEED_NAME = "apifailures"

logging.basicConfig(
        format='%(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
sensor_failures = 0
api_failures = 0

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    has_data = False
    tempf = None

    if humidity is not None and temperature is not None:
        tempf = round((temperature * 1.8) + 32, 1)
        humidity = round(humidity, 1)
        logging.info("Temp={0:0.1f}*F Humidity={1:0.1f}%".format(tempf, humidity))
        has_data = True
        sensor_failures = 0
    else:
        logging.warning("Sensor reading failed!")
        sensor_failures += 1

    try:
        if has_data:
            aio.send(TEMP_FEED_NAME, tempf)
            aio.send(HUMIDITY_FEED_NAME, humidity)

        aio.send(SENSOR_FAILURES_FEED_NAME, sensor_failures)
        aio.send(API_FAILURES_FEED_NAME, api_failures)

        api_failures = 0
        sensor_failures = 0 # successfully logged; reset value
    except:
        logging.error("Failed sending data!")
        api_failures += 1

    time.sleep(DELAY)
