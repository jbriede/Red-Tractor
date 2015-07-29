import RPi.GPIO as GPIO
import time

#Reads the Sonar Sensor
def readsonar(TRIG,ECHO):
    GPIO.output(TRIG,1) #begin Trigger pulse
    time.sleep(0.00001)
    GPIO.output(TRIG,0) #end Trigger pulse
    begin = time.time()
    while GPIO.input(ECHO) == 0: #wait for Trigger pulse
        if ((time.time() - begin) * 1700) >= 30.0: # if no object is encountered.. stop looking
            return 30
    start = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()
    dist = (stop - start) * 17000
    time.sleep(0.05)
    return int(dist)

#SonarSense averages ten measurements
def SonarSense(TRIG,ECHO):
    L = [0,0,0,0,0,0,0,0,0,0,0]
    for x in range(11):
        dist_new = readsonar(TRIG,ECHO)
        L[x] = int(dist_new)
    L = sorted(L)
    dist = L[10]
    return dist

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def IRSense(IRS0, SPICLK, SPIMOSI, SPIMISO, SPICS):
    measure_tot = 0
    for x in range(30):
        measure_new = readadc(IRS0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        measure_tot = measure_tot + measure_new
    measure_avg = (measure_tot / 30)
    if (measure_avg < 200):
        zone = 3
    elif ((measure_avg < 350) & (measure_avg > 200)):
        zone = 2
    elif ((measure_avg < 1024) & (measure_avg > 350)):
        zone = 1
    else:
        return -1
    return zone
