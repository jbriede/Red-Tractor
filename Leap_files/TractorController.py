import Leap
import sys
import json
import time
import datetime
import socket
#UDP Setup
UDP_IP = " 10.0.7.52"
UDP_PORTIN = 5005
UDP_PORTOUT = 5006

UDP_PORT = 5006

left_hand_speed = 0


class DataReadListener(Leap.Listener):
    def __init__(self):
        super(DataReadListener, self).__init__()
        self.data_buffer = []

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        #self.data_buffer.append(FrameData(frame))
        hands = frame.hands
        first_hand = hands[0]
        second_hand = hands[1]
        #hand = hands.rightmost
        if (first_hand.palm_position.x<second_hand.palm_position.x):
            left_hand_pos = first_hand.palm_position.z*-1
            right_hand_pos = second_hand.palm_position.z*-1
        else:
            right_hand_pos = first_hand.palm_position.z*-1
            left_hand_pos = second_hand.palm_position.z*-1
        #print "hand 1: %d, hand 2: %d" % ((int)(first_hand.palm_position.z*-1), (int)(second_hand.palm_position.z*-1))
        print "left: %d, right: %d" % (left_hand_pos, right_hand_pos)
        #print "hand 1: %d, hand 2: %d" % ((int)(first_hand.palm_position.x), (int)(second_hand.palm_position.x))

        MESSAGE = ""

        if right_hand_pos<0:
            MESSAGE+='0'
        else:
            MESSAGE+='1'

        if left_hand_pos<0:
            MESSAGE+='0'
        else:
            MESSAGE+='1'


        if abs(right_hand_pos)<40:
            right_hand_speed = 0
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<65:
            right_hand_speed = 1
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<85:
            right_hand_speed = 2
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<105:
            right_hand_speed = 3
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<120:
            right_hand_speed = 4
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<135:
            right_hand_speed = 5
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<150:
            right_hand_speed = 6
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<165:
            right_hand_speed = 7
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<180:
            right_hand_speed = 8
            MESSAGE+=str(right_hand_speed)
        elif abs(right_hand_pos)<250:
            right_hand_speed = 9
            MESSAGE+=str(right_hand_speed)
        #print MESSAGE
        #MESSAGE = "0000"


        if abs(left_hand_pos)<40:
            left_hand_speed = 0
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<65:
            left_hand_speed = 1
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<85:
            left_hand_speed = 2
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<105:
            left_hand_speed = 3
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<120:
            left_hand_speed = 4
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<135:
            left_hand_speed = 5
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<150:
            left_hand_speed = 6
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<165:
            left_hand_speed = 7
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<180:
            left_hand_speed = 8
            MESSAGE+=str(left_hand_speed)
        elif abs(left_hand_pos)<250:
            left_hand_speed = 9
            MESSAGE+=str(left_hand_speed)

        if len(MESSAGE)!=4:
            MESSAGE="0000"

#print MESSAGE

        sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        time.sleep(.5);

        # Give some feedback to user
        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              #frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))


def main():
    # Create a sample listener and controller
    listener = DataReadListener()
    controller = Leap.Controller()

    print "Press Enter to start tracking, press Enter again to stop..."
    sys.stdin.readline()

    controller.add_listener(listener)

    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

    print "Done!"


if __name__ == "__main__":
    main()
