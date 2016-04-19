# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 17:02:48 2016

@author: harshad
"""

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import Adafruit_DHT
import time
from pubnub import Pubnub


app = Flask(__name__)

api = Api(app)

sensor = Adafruit_DHT.DHT22
pin = 4
 

                     
            
if __name__ == '__main__':
    app.run(debug=True)
    
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        data='Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        pubnub = Pubnub(publish_key="pub-c-d3bae2e1-d58c-457c-bee1-4fd8bb7c8992", subscribe_key="sub-c-915d6d7c-615c-11e5-9a34-02ee2ddab7fe")
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
      
      
        pubnub.subscribe(channels='my_channel', callback=callback, error=callback,
                         connect=connect, reconnect=reconnect, disconnect=disconnect)

        pubnub.publish('my_channel', {
                    'columns': [
                        ['x', time.time()],
                        ['temperature_celcius', temperature]
                        ]

                    });           
          
    except Exception as e:
        print 'error',str(e)
   

