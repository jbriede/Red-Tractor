import RPi.GPIO as GPIO
import time

## Motor Control Functions
# Forward
# Reverse
# Turn Right
# Turn Left
# Soft Right
# Soft Left
# All Stop

# Min1 = right forward
# Min2 = right backward
# Min3 = left backward
# Min4 = left forward
   
def DriveForward(Min1,Min2,Min3,Min4, moving, delay):
    if (moving):
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
        GPIO.output(Min1, 1)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0) 
        GPIO.output(Min4, 1)
        time.sleep(delay)
   
def DriveBackward(Min1,Min2,Min3,Min4, moving, delay):
    if (moving):
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 1)
        GPIO.output(Min3, 1)
        GPIO.output(Min4, 0)
        time.sleep(delay)
    
def TurnRight(Min1,Min2,Min3,Min4, moving, delay):
    if (moving):
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 1)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 1)
        time.sleep(delay)

def SoftRight(Min1,Min2,Min3,Min4, moving, delay):
    if (moving):
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 1)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
    
   
def TurnLeft(Min1,Min2,Min3,Min4, moving, delay):
    if (moving):
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
        GPIO.output(Min1, 1)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 1)
        GPIO.output(Min4, 0)
        time.sleep(delay)

def SoftLeft(Min1,Min2,Min3,Min4, moving, delay):
    if (moving):
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 0)
        GPIO.output(Min4, 0)
        time.sleep(delay)
        GPIO.output(Min1, 0)
        GPIO.output(Min2, 0)
        GPIO.output(Min3, 1)
        GPIO.output(Min4, 0)
        time.sleep(delay)

def StopMotor(Min1,Min2,Min3,Min4):
    GPIO.output(Min1, 0)
    GPIO.output(Min2, 0)
    GPIO.output(Min3, 0)
    GPIO.output(Min4, 0)
