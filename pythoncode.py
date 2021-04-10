
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json

#Provide your IBM Watson Device Credentials
organization = "1wwfmh"
deviceType = "iotdevice"
deviceId = "1357"
authMethod = "token"
authToken = "135792468"


# Initialize the device client.
T=0
H=0
waterlevel=0

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='lighton':
                print("LIGHT ON IS RECEIVED")
                
                
        elif cmd.data['command']=='lightoff':
                print("LIGHT OFF IS RECEIVED")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        waterlevel=int(input("enter water level:"))

        if(waterlevel>=900):
            print("open 6 dam gates")
        elif(waterlevel>=700):
            print("open 4 dam gates")
        elif(waterlevel>=500):
            print("open 2 gates")
                #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'waterlevel' : waterlevel}}
        #print data
        def myOnPublishCallback():
            print ("Published waterlevel = %s" %waterlevel ,"to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
