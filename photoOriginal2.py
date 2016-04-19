#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import Adafruit_DHT
import time
from pubnub import Pubnub
import RPi.GPIO as GPIO, time, os      
import json
import urllib2




DEBUG = 1
GPIO.setmode(GPIO.BCM)
status = 0

        


if __name__ == '__main__':
        
        def callback(message, channel):
                print(message)
          
              
        def error(message):
                print("ERROR : " + str(message))
                  
                  
        def connect(message):
                print("CONNECTED")
                print pubnub.publish(channel='my_channel', message='Hello from the PubNub Python SDK')
                  
                  
                  
        def reconnect(message):
                print("RECONNECTED")
                  
                  
        def disconnect(message):
                print("DISCONNECTED")
              

        pubnub = Pubnub(publish_key="pub-c-d3bae2e1-d58c-457c-bee1-4fd8bb7c8992", subscribe_key="sub-c-915d6d7c-615c-11e5-9a34-02ee2ddab7fe")            
        def RCtime (RCpin):
                reading = 0
                GPIO.setup(RCpin, GPIO.OUT)
                GPIO.output(RCpin, GPIO.LOW)
                time.sleep(0.1)

                GPIO.setup(RCpin, GPIO.IN)
                # This takes about 1 millisecond per loop cycle
                while (GPIO.input(RCpin) == GPIO.LOW):
                        reading += 1
                return reading
                
        while True:                                     
                '''print RCtime(18)     # Read RC timing using pin #18'''
              
                if(RCtime(18)>350):
                        '''print 0'''
                        global status
                        status = 0
                else:
                        '''print 1'''
                        global status
                        status = 1

                print status
                photoData={
                    "device_id" : "tv1",
                    "device_type" : "tv",
                    "channel" : "ch1",
                    "date" : "2016-04-12",
                    "value" : status }

                req = urllib2.Request('http://10.0.0.227:4000/devices')
                req.add_header('Content-Type', 'application/json')
                response=urllib2.urlopen(req,json.dumps(photoData))
                print 'response',response
                pubnub.subscribe(channels='my_channel', callback=callback, error=callback,connect=connect, reconnect=reconnect, disconnect=disconnect)
                pubnub.publish('my_channel', {
                    'columns': [
                        ['x', time.time()],
                        ['tv_operating_status', status]
                        ]

                    });      
