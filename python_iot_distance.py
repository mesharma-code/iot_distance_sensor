#Libraries
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqttClient
import paho.mqtt.publish as publish
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
ledPin=4
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

client = mqttClient.Client("Python")
GPIO.setup(ledPin, GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(3)
            if (dist < 50 ):
                print("Object Close!")
               # client.publish("test/message","Hello from Pi")
                publish.single("test/message", "Hello from Pi: Getting Close %.1f cm away" % dist, hostname="192.168.x.x")
                GPIO.output(ledPin,GPIO.HIGH)
                print("LED lit")
                time.sleep(3)
                GPIO.output(ledPin, GPIO.LOW)

 
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


