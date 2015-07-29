import RPi.GPIO as GPIO
## Motor Control Functions
#Forward
#Reverse
#Turn Right
#Turn Left
#Soft Right
#Soft Left
#All Stop
   
def DriveForward(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 1)
    GPIO.output(Min2, 0)
    GPIO.output(Min3, 0)
    GPIO.output(Min4, 1)
   
def DriveBackward(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 0)
    GPIO.output(Min2, 1)
    GPIO.output(Min3, 1)
    GPIO.output(Min4, 0)
    
def TurnRight(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 0)
    GPIO.output(Min2, 1)
    GPIO.output(Min3, 0)
    GPIO.output(Min4, 1)

def SoftRight(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 0)
    GPIO.output(Min2, 1)
    GPIO.output(Min3, 0)
    GPIO.output(Min4, 0)    
   
def TurnLeft(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 1)
    GPIO.output(Min2, 0)
    GPIO.output(Min3, 1)
    GPIO.output(Min4, 0)

def SoftLeft(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 0)
    GPIO.output(Min2, 0)
    GPIO.output(Min3, 1)
    GPIO.output(Min4, 0)    

def StopMotor(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 0)
    GPIO.output(Min2, 0)
    GPIO.output(Min3, 0)
    GPIO.output(Min4, 0)
