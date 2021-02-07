import os, sys, inspect, thread, time, math
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

lPrevPalmX = rPrevPalmX = lPrevPalmY = rPrevPalmY = lPrevPalmZ = rPrevPalmZ = 0.0
f=open("result.csv",'a')

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        
        
        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        global f
        slname=input("input slname : ")
        f.write(',' + slname + '\n')
        print "Exited"
        

    def on_frame(self, controller):

        global lPrevPalmX, rPrevPalmX, lPrevPalmY, rPrevPalmY, lPrevPalmZ, rPrevPalmZ, f

        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # Get hands
        leftExist = False
        rightExist = False
        for hand in frame.hands:
            if hand.is_left:
                leftExist = True
            if hand.is_right:
                rightExist = True

        if not leftExist and rightExist:
            # print "[",
            list = []

            for i in range(13):
                list.append(0)
            
            

            for hand in frame.hands:

                palmX = palmY = palmZ = 0.0

                handType = "Right hand"

                tempPalm = hand.palm_position
                palmTotal = str(tempPalm).replace("(", "").replace(")", "")

                palmX = float(palmTotal.split(',')[0])
                palmY = float(palmTotal.split(',')[1])
                palmZ = float(palmTotal.split(',')[2])

                rPalmDist = math.sqrt(math.pow(palmX - rPrevPalmX, 2) + math.pow(palmY - rPrevPalmY, 2) + math.pow(palmZ - rPrevPalmZ, 2))
                # print "rPalmDist : %f" % (rPalmDist),
                list.insert(13,rPalmDist)

                rPrevPalmX = palmX
                rPrevPalmY = palmY
                rPrevPalmZ = palmZ

                # Get the hand's normal vector and direction
                normal = hand.palm_normal
                direction = hand.direction

                # Calculate the hand's pitch, roll, and yaw angles
                '''
                print "pitch: %f, roll: %f, yaw: %f" % (
                    direction.pitch * Leap.RAD_TO_DEG,
                    normal.roll * Leap.RAD_TO_DEG,
                    direction.yaw * Leap.RAD_TO_DEG),
                '''
                list.insert(14,direction.pitch * Leap.RAD_TO_DEG)
                list.insert(15,normal.roll * Leap.RAD_TO_DEG)
                list.insert(16,direction.yaw * Leap.RAD_TO_DEG)

                # Get arm bone
                    
                # Get fingers

                thumbX = thumbY = thumbZ = indexX = indexY = indexZ = middleX = middleY = middleZ = ringX = ringY = ringZ = pinkyX = pinkyY = pinkyZ = 0.0

                for finger in hand.fingers:
                    # Get bones
                    bone = finger.bone(3)
                    tempDistal = bone.next_joint
                    distalTotal = str(tempDistal).replace("(", "").replace(")", "")
                        
                    if self.finger_names[finger.type] == "Thumb":
                        thumbX = float(distalTotal.split(',')[0])
                        thumbY = float(distalTotal.split(',')[1])
                        thumbZ = float(distalTotal.split(',')[2])

                    elif self.finger_names[finger.type] == "Index":
                        indexX = float(distalTotal.split(',')[0])
                        indexY = float(distalTotal.split(',')[1])
                        indexZ = float(distalTotal.split(',')[2])
                        
                    elif self.finger_names[finger.type] == "Middle":
                        middleX = float(distalTotal.split(',')[0])
                        middleY = float(distalTotal.split(',')[1])
                        middleZ = float(distalTotal.split(',')[2])

                    elif self.finger_names[finger.type] == "Ring":
                        ringX = float(distalTotal.split(',')[0])
                        ringY = float(distalTotal.split(',')[1])
                        ringZ = float(distalTotal.split(',')[2])

                    elif self.finger_names[finger.type] == "Pinky":
                        pinkyX = float(distalTotal.split(',')[0])
                        pinkyX = float(distalTotal.split(',')[1])
                        pinkyZ = float(distalTotal.split(',')[2])

                thumbToIndex = math.sqrt(math.pow(thumbX - indexX, 2) + math.pow(thumbY - indexY, 2) + math.pow(thumbZ - indexZ, 2))
                indexToMiddle = math.sqrt(math.pow(indexX - middleX, 2) + math.pow(indexY - middleY, 2) + math.pow(indexZ - middleZ, 2))
                middleToRing = math.sqrt(math.pow(middleX - ringX, 2) + math.pow(middleY - ringY, 2) + math.pow(middleZ - ringZ, 2))
                ringToPinky = math.sqrt(math.pow(ringX - pinkyX, 2) + math.pow(ringY - pinkyY, 2) + math.pow(ringZ - pinkyZ, 2))
                # print "thumbToIndex : %f, indexToMiddle : %f, middleToRing : %f, ringToPinky : %f" % (thumbToIndex, indexToMiddle, middleToRing, ringToPinky),
                list.insert(17,thumbToIndex)
                list.insert(18,indexToMiddle)
                list.insert(19,middleToRing)
                list.insert(20,ringToPinky)

                thumbToPalm = math.sqrt(math.pow(thumbX - palmX, 2) + math.pow(thumbY - palmY, 2) + math.pow(thumbZ - palmZ, 2))
                indexToPalm = math.sqrt(math.pow(indexX - palmX, 2) + math.pow(indexY - palmY, 2) + math.pow(indexZ - palmZ, 2))
                middleToPalm = math.sqrt(math.pow(middleX - palmX, 2) + math.pow(middleY - palmY, 2) + math.pow(middleZ - palmZ, 2))
                ringToPalm = math.sqrt(math.pow(ringX - palmX, 2) + math.pow(ringY - palmY, 2) + math.pow(ringZ - palmZ, 2))
                pinkyToPalm = math.sqrt(math.pow(pinkyX - palmX, 2) + math.pow(pinkyY - palmY, 2) + math.pow(pinkyZ - palmZ, 2))
                # print "thumbToPalm : %f, indexToPalm : %f, middleToPalm : %f, ringToPalm : %f, pinkyToPalm : %f" % (thumbToPalm, indexToPalm, middleToPalm, ringToPalm, pinkyToPalm),
                list.insert(21,thumbToPalm)
                list.insert(22,indexToPalm)
                list.insert(23,middleToPalm)
                list.insert(24,ringToPalm)
                list.insert(25,pinkyToPalm)

            for i in list:
                print i,
                data = ("%f " % i)
                f.write(data)
            # print "] end!"
            

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
