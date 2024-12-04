import RPi.GPIO as GPIO
import dht11
import time
import datetime

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)


instance = dht11.DHT11(pin=17)


while True:
    result = instance.read()
    if result.is_valid():
        print("Time: " + str(datetime.datetime.now()))
        print("Temperature: " + str(result.temperature) + " C")
        print("Humidity: " + str(result.humidity) + " %")
        time.sleep(3)
        print()
