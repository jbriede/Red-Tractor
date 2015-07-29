import RPi.GPIO as GPIO
import time
import motor
import sensor

#SETUP
GPIO.setmode(GPIO.BOARD)

Min1 = 35 #Motor Enable Pins
Min2 = 37
Min3 = 32
Min4 = 36
TRIG = 38 #Sonar Trigger Pin
ECHO = 40 #Sonar Echo Pin
SPICLK = 7 #ADC_CLK
SPIMISO = 29 #ADC_DOUT
SPIMOSI = 31 #ADC_DIN
SPICS = 33   #ADC_Chip_Select
IRS0 = 0

GPIO.setup(Min1, GPIO.OUT)
GPIO.output(Min1, 0)
GPIO.setup(Min2, GPIO.OUT)
GPIO.output(Min2, 0)
GPIO.setup(Min3, GPIO.OUT)
GPIO.output(Min3, 0)
GPIO.setup(Min4, GPIO.OUT)
GPIO.output(Min4, 0)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, 0)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
time.sleep(0.1)

#Motor function definitions
#(Min1,Min2,Min3,Min4)
Forward = motor.DriveForward
Reverse = motor.DriveBackward
Right = motor.TurnRight
Left = motor.TurnLeft
SRight = motor.SoftRight
SLeft = motor.SoftLeft
Stop = motor.StopMotor

#Sensor function definitions
#(TRIG,ECHO)
#(IRS0, SPICLK, SPIMOSI, SPIMISO, SPICS)
SonarSense = sensor.SonarSense
IRSense = sensor.IRSense


print "Track start"
print " "

##for i in range(12):
##    dist = SonarSense(TRIG, ECHO)
##    print dist
##    time.sleep(1)

Forward(Min1,Min2,Min3,Min4)
time.sleep(5)
    
Stop(Min1,Min2,Min3,Min4)
time.sleep(2)

Reverse(Min1,Min2,Min3,Min4)
time.sleep(3)

Stop(Min1,Min2,Min3,Min4)
time.sleep(2)

Right(Min1,Min2,Min3,Min4)
time.sleep(3)

Stop(Min1,Min2,Min3,Min4)
time.sleep(2)

Left(Min1,Min2,Min3,Min4)
time.sleep(3)

Stop(Min1,Min2,Min3,Min4)
time.sleep(2)

print "Track End " 


GPIO.cleanup()
