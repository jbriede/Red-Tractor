import RPi.GPIO as GPIO
import time
import motor2
import sensor
import socket


#UDP Setup
UDP_IP = "127.0.0.1"
UDP_PORTIN = 5006
UDP_PORTOUT = 5005


#GPIO Setup
GPIO.setmode(GPIO.BOARD)
Min1 = 35 #Motor Enable Pins
Min2 = 37
Min3 = 32
Min4 = 36
TRIG1 = 38 #Sonar Trigger Pin
ECHO1 = 40 #Sonar Echo Pin
TRIG2 = 16 #Sonar Trigger Pin
ECHO2 = 18 #Sonar Echo Pin
SPICLK = 7 #ADC_CLK
SPIMISO = 29 #ADC_DOUT
SPIMOSI = 31 #ADC_DIN
SPICS = 33   #ADC_Chip_Select
IRS0 = 0
IRS1 = 1

GPIO.setwarnings(False)
GPIO.setup(Min1, GPIO.OUT)
GPIO.setup(Min2, GPIO.OUT)
GPIO.setup(Min3, GPIO.OUT)
GPIO.setup(Min4, GPIO.OUT)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.output(TRIG1, 0)
GPIO.output(TRIG2, 0)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
time.sleep(0.1)


#Motor function definitions
#(Min1,Min2,Min3,Min4)
Forward = motor2.DriveForward
Reverse = motor2.DriveBackward
Right = motor2.TurnRight
Left = motor2.TurnLeft
SRight = motor2.SoftRight
SLeft = motor2.SoftLeft
Stop = motor2.StopMotor


#Sensor function definitions
#(TRIG,ECHO)
#(IRS0, SPICLK, SPIMOSI, SPIMISO, SPICS)
SonarSense = sensor.SonarSense
IRSense = sensor.IRSense

#UDP initialization
sock = socket.socket(socket.AF_INET, #Internet
                     socket.SOCK_DGRAM) #UDP
sock.bind((UDP_IP, UDP_PORTIN))


#Infinite loop
dataprev = 'stop'
idist1 = '0'
idist2 = '0'
sensor = "0000"
delay = .005
moving = False

try:
    while True:
        data, addr = sock.recvfrom(1024)                        #buffer size is 1024 bytes
        data = str(data)
        data = data.strip()
        print "received message: ", data                        #print recieved data package

        if (data[1]=='1'):
            delay = .09;

        elif (data[1] == '2'):
            delay = .07

        elif (data[1] == '3'):
            delay = .05

        elif (data[1] == '4'):
            delay = .02

        elif (data[1] == '5'):
            delay = .009

        elif (data[1] == '6'):
            delay = .006

        elif (data[1] == '7'):
            delay = .003

        elif (data[1] == '8'):
            delay = .001

        else:
            delay = .03

        print delay

        #dist1 = SonarSense(TRIG1,ECHO1)                            #read sensor data
        #sdist2 = SonarSense(TRIG2,ECHO2)                           #read sensor data
        #if (moving == True):                                       #read IR sensor if RDRIV is moving
        #idist1 = IRSense(IRS0, SPICLK, SPIMOSI, SPIMISO, SPICS)    #read front IR sensor
        #idist2 = IRSense(IRS1, SPICLK, SPIMOSI, SPIMISO, SPICS)    #read rear IR sensor
        #sensor = str(sdist1) + '.' + str(sdist2) + '.' + str(idist1)+ '.' + str(idist2) + '.'
        sock.sendto(sensor, (UDP_IP, UDP_PORTOUT))                  #send sensor string

        #if new instruction is different from the previous
        if (data != dataprev):
            dataprev = data
            print 'new instruct'

        if ("f" in data):
            print 'moving Forward'
            moving = True
            Forward(Min1,Min2,Min3,Min4, moving, delay)

        elif ("b" in data):
            Reverse(Min1,Min2,Min3,Min4, moving, delay)
            print 'moving Backwards'
            moving = True

        elif ("r" in data):
            Right(Min1,Min2,Min3,Min4, moving, delay)
            print 'moving Right'
            moving = True

        elif ("l" in data):
            Left(Min1,Min2,Min3,Min4, moving, delay)
            print 'moving Left'
            moving = True

        elif ("a" in data):
            SLeft(Min1,Min2,Min3,Min4, moving, delay)
            print 'moving Soft Left'
            moving = True

        elif ("c" in data):
            SRight(Min1,Min2,Min3,Min4,moving, delay)
            print 'moving Soft Right'
            moving = True

        else: 
            Stop(Min1,Min2,Min3,Min4)
            print 'stopped'
            moving = False
               
        print sensor
           
except KeyboardInterrupt:
    GPIO.cleanup()
