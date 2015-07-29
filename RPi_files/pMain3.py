import RPi.GPIO as GPIO
import time
import socket
import random


#UDP Setup
UDP_IP = "127.0.0.1"
UDP_PORTIN = 5006
UDP_PORTOUT = 5005


#GPIO Setup
GPIO.setmode(GPIO.BOARD)
Min1 = 35  # right forward
Min2 = 37  # right backward
Min3 = 32  # left backward
Min4 = 36  # left forward

GPIO.setwarnings(False)
GPIO.setup(Min1, GPIO.OUT)
GPIO.setup(Min2, GPIO.OUT)
GPIO.setup(Min3, GPIO.OUT)
GPIO.setup(Min4, GPIO.OUT)
time.sleep(0.1)


#UDP initialization
sock = socket.socket(socket.AF_INET, #Internet
                     socket.SOCK_DGRAM) #UDP
sock.bind(('', UDP_PORTIN)) #socket.gethostname()


#Infinite loop
sensor = "0000"
print "\nBEGIN"

try:
    
    while True:

        print "--------------------------------"
        
        # read data message from arduino
        data, addr = sock.recvfrom(1024)
        if (len(data) == 4 | len(data) == 12): 
            data = str(data)
        data = data.strip()
        print "received message: ", data
        sock.sendto('', (UDP_IP, UDP_PORTOUT))

        # data[0] = right_direction
        # data[1] = left_direction
        # data[2] = right_speed
        # data[3] = left_speed

        #if (len(data) == 4 | len(data) == 12):
        right_direction = int(float(data[0]))
        print "right_direction: ", right_direction
        left_direction = int(float(data[1]))
        print "left_direction: ", left_direction
                  
        right_speed = int(float(data[2]))
        print "right_speed: ", right_speed
        left_speed = int(float(data[3]))
        print "left_speed: ", left_speed


        # set a total time
        total = .01


        # define delays
        
        if (right_speed >= left_speed):

            if   (data[2] == '1'):
                delay = .009

            elif (data[2] == '2'):
                delay = .008

            elif (data[2] == '3'):
                delay = .007
                
            elif (data[2] == '4'):
                delay = .006

            elif (data[2] == '5'):
                delay = .005

            elif (data[2] == '6'):
                delay = .003

            elif (data[2] == '7'):
                delay = .002

            elif (data[2] == '8'):
                delay = .001

            elif (data[2] == '9'):
                delay = 0

            else:
                delay = .005


        elif (right_speed < left_speed):

            if   (data[3] == '1'):
                delay = .009

            elif (data[3] == '2'):
                delay = .008

            elif (data[3] == '3'):
                delay = .007
                
            elif (data[3] == '4'):
                delay = .006

            elif (data[3] == '5'):
                delay = .005

            elif (data[3] == '6'):
                delay = .003

            elif (data[3] == '7'):
                delay = .002

            elif (data[3] == '8'):
                delay = .001

            elif (data[3] == '9'):
                delay = 0

            else:
                delay = .005

            

        print "delay: ", delay


        # 9 Cases
        # rightS>leftS, rightD==0, leftD==0 -- backward, turning left
        # rightS>leftS, rightD==0, leftD==1 -- !IMPOSIBLE!
        # rightS>leftS, rightD==1, leftD==1 -- forward, turning left

        # rightS<leftS, rightD==0, leftD==0 -- backward, turning right
        # rightS<leftS, rightD==1, leftD==0 -- !IMPOSIBLE!
        # rightS<leftS, rightD==1, leftD==1 -- forward, turning right

        # rightD==1, leftD==0, ~rightS==leftS==0 -- hard left turn
        # rightD==0, leftD==1, ~rightS==leftS==0 -- hard right turn
        
        # rightS=leftS!=0, rightD==leftD==1 -- forward
        # rightS=leftS!=0, rightD==leftD==0 -- backward

        # rightS==leftS==0 -- stopped

        # none of the above -- ERROR, stop motors



        # -- backward, turning left
        if ( (right_speed>left_speed) & (right_direction==0) & (left_direction==0) ):

            print "backward, turning left"
            
            # define slow and fast motors
            print "fast: ", right_speed
            print "slow: ", left_speed

            # find difference
            difference = right_speed - left_speed
            print "difference: ", difference

            for c in range(0, 8):

                # get random number between 1 and 9
                number = random.randint(1,9)

                if ( (number>difference) & (left_speed!=0) ):
                    # slower motors ON
                    # right backward, left backward
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 0) 
                    GPIO.output(Min2, 1)
                    GPIO.output(Min3, 1)
                    GPIO.output(Min4, 0)
                    time.sleep((total-delay))
                    print "on"

                            
                else:
                    # slower motors OFF
                    # right backward, left OFF
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 0) 
                    GPIO.output(Min2, 1)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep((total-delay))
                    print "off"

 

        # -- forward, turning left
        elif ( (right_speed>left_speed) & (right_direction==1) & (left_direction==1) ):

            print "forward, turning left"
            
            # define slow and fast motors
            print "fast: ", right_speed
            print "slow: ", left_speed

            # find difference
            difference = right_speed - left_speed
            print "difference: ", difference
            
            for c in range(0, 8):

                number = random.randint(1,9)
                
                if ( (number>difference) & (left_speed!=0) ):
                    # turn slower motors ON
                    # right forward, left forward
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 1) 
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 1)
                    time.sleep((total-delay))
                    print "on"

                                
                else:
                    # turn slower motors OFF
                    # right forward, left OFF
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 1) 
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep((total-delay))
                    print "off"



        # -- backward, turning right
        elif ( (right_speed<left_speed) & (right_direction==0) & (left_direction==0) ):

            print "bakward, turning right"
                
            # define slow and fast motors
            print "fast: ", left_speed
            print "slow: ", right_speed

            # find difference
            difference = left_speed - right_speed
            print "difference: ", difference
                
            for c in range(0, 8):

                # get random number between 1 and 9
                number = random.randint(1,9)

                if ( (number>difference) & (right_speed!=0) ):
                    # turn slower motors ON
                    # right backward, left backward
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 0) 
                    GPIO.output(Min2, 1)
                    GPIO.output(Min3, 1)
                    GPIO.output(Min4, 0)
                    time.sleep((total-delay))
                    print "on"

                            
                else:
                    # turn slower motors OFF
                    # right OFF, left backward
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 0) 
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 1)
                    GPIO.output(Min4, 0)
                    time.sleep((total-delay))
                    print "off"



        # -- forward, turning right
        elif ( (right_speed<left_speed) & (right_direction>0) & (left_direction>0) ):

            print "forward, turning right"
            
            # define slow and fast motors
            print "fast: ", left_speed
            print "slow: ", right_speed

            # find difference
            difference = left_speed - right_speed
            print "difference: ", difference

            for c in range(0, 8):

                # get random number between 1 and 9
                number = random.randint(1,9)

                if ( (number>difference) & (right_speed!=0) ):
                    # turn slower motors ON
                    # right forward, left forward
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 1) 
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 1)
                    time.sleep((total-delay))
                    print "on"
                        
                else:
                    # turn slower motors OFF
                    # right OFF, left forward
                    GPIO.output(Min1, 0)
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 0)
                    time.sleep(delay)
                    GPIO.output(Min1, 0) 
                    GPIO.output(Min2, 0)
                    GPIO.output(Min3, 0)
                    GPIO.output(Min4, 1)
                    time.sleep((total-delay))
                    print "off"



        # -- hard left 
        elif ( (right_direction==1) & (left_direction==0) & (~(right_speed==left_speed==0)) ):

            print "hard left turn"
            
            if ( right_speed > left_speed ):
            
                # define slow and fast motors
                print "fast: ", right_speed
                print "slow: ", left_speed

                # find difference
                difference = right_speed - left_speed
                print "difference: ", difference             
                    
                for c in range(0, 8):

                    # get random number between 1 and 9
                    number = random.randint(1,9)

                    if (number > difference):
                        # turn slower motors ON
                        # right forward, left backward
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 1) 
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 1)
                        GPIO.output(Min4, 0)
                        time.sleep((total-delay))
                        print "on"
   
                    else:
                        # turn slower motors OFF
                        # right forward, left OFF
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 1) 
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep((total-delay))
                        print "off"


            elif ( right_speed < left_speed ):

                # define slow and fast motors
                print "fast: ", left_speed
                print "slow: ", right_speed

                # find difference
                difference = left_speed - right_speed
                print "difference: ", difference             
                    
                for c in range(0, 8):

                    # get random number between 1 and 9
                    number = random.randint(1,9)

                    if (number > difference):
                        # turn slower motors ON
                        # right forward, left backward
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 1) 
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 1)
                        GPIO.output(Min4, 0)
                        time.sleep((total-delay))
                        print "on"

                    else:
                        # turn slower motors OFF
                        # right OFF, left backward
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 0) 
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 1)
                        GPIO.output(Min4, 0)
                        time.sleep((total-delay))
                        print "off"

            elif ( right_speed == left_speed ):

                print "speed: ", right_speed

                # set right motors forward,
                # left motors backward
                GPIO.output(Min1, 0)
                GPIO.output(Min2, 0)
                GPIO.output(Min3, 0)
                GPIO.output(Min4, 0)
                time.sleep(((delay)*10))
                GPIO.output(Min1, 1)
                GPIO.output(Min2, 0)
                GPIO.output(Min3, 1)
                GPIO.output(Min4, 0)
                time.sleep(((total-delay)*10))



        # -- hard right 
        elif ( (right_direction==0) & (left_direction==1) & (~(right_speed==left_speed==0)) ):

            print "hard right turn"

            if ( right_speed > left_speed ):

                # define fast and slow motors
                print "fast: ", right_speed
                print "slow: ", left_speed

                # find difference
                difference = right_speed - left_speed
                print "difference: ", difference

                for c in range(0, 8):

                    # get random number between 1 and 9
                    number = random.randint(1,9)

                    if (number > difference):
                        # turn slower motors ON
                        # right backward, left forward
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 0) 
                        GPIO.output(Min2, 1)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 1)
                        time.sleep((total-delay))
                        print "on"

                    else:
                        # turn slower motors OFF
                        # right backward, left OFF
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 0) 
                        GPIO.output(Min2, 1)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep((total-delay))
                        print "off"


            elif ( right_speed < left_speed ):

                # define fast and slow motors
                print "fast: ", left_speed
                print "slow: ", right_speed

                # find difference
                difference = left_speed - right_speed
                print "difference: ", difference

                for c in range(0, 8):

                    # get random number between 1 and 9
                    number = random.randint(1,9)

                    if (number > difference):
                        # turn slower motors ON
                        # right backward, left forward
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 0) 
                        GPIO.output(Min2, 1)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 1)
                        time.sleep((total-delay))
                        print "on"

                        
                    else:
                        # turn slower motors OFF
                        # right OFF, left forward
                        GPIO.output(Min1, 0)
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 0)
                        time.sleep(delay)
                        GPIO.output(Min1, 0) 
                        GPIO.output(Min2, 0)
                        GPIO.output(Min3, 0)
                        GPIO.output(Min4, 1)
                        time.sleep((total-delay))
                        print "off"


            elif ( right_speed == left_speed ):

                print "speed: ", right_speed

                # set left motors forward,
                # right motors backward
                GPIO.output(Min1, 0)
                GPIO.output(Min2, 0)
                GPIO.output(Min3, 0)
                GPIO.output(Min4, 0)
                time.sleep(((delay)*10))
                GPIO.output(Min1, 0)
                GPIO.output(Min2, 1)
                GPIO.output(Min3, 0)
                GPIO.output(Min4, 1)
                time.sleep(((total-delay)*10))



        # -- moving forward            
        elif ( (right_speed==left_speed!=0) & (right_direction==left_direction==1) ):

            print "direction: forward"
            print "speed: ", right_speed

            # set motors forward
            GPIO.output(Min1, 0)
            GPIO.output(Min2, 0)
            GPIO.output(Min3, 0)
            GPIO.output(Min4, 0)
            time.sleep(((delay)*10))
            GPIO.output(Min1, 1)
            GPIO.output(Min2, 0)
            GPIO.output(Min3, 0)
            GPIO.output(Min4, 1)
            time.sleep(((total-delay)*10))
            
            

        # -- moving backward         
        elif ( (right_speed==left_speed!=0) & (right_direction==left_direction==0) ):

            print "direction: backward"
            print "speed: ", right_speed

            # set motors backward
            GPIO.output(Min1, 0)
            GPIO.output(Min2, 0)
            GPIO.output(Min3, 0)
            GPIO.output(Min4, 0)
            time.sleep(((delay)*10))
            GPIO.output(Min1, 0)
            GPIO.output(Min2, 1)
            GPIO.output(Min3, 1)
            GPIO.output(Min4, 0)
            time.sleep(((total-delay)*10))



        # -- stopped
        elif ( (right_speed==0) & (left_speed==0) ):

            # stop the motors
            GPIO.output(Min1, 0)
            GPIO.output(Min2, 0)
            GPIO.output(Min3, 0)
            GPIO.output(Min4, 0)
            print "stopped"


        # -- none of the above
        else:
            
            # stop the motors
            GPIO.output(Min1, 0)
            GPIO.output(Min2, 0)
            GPIO.output(Min3, 0)
            GPIO.output(Min4, 0)
            print "ERROR -- stopping"



except KeyboardInterrupt:
    GPIO.cleanup()
