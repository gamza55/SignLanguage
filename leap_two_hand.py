import os, sys, inspect, thread, time, math
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = './lib/x64' if sys.maxsize > 2**32 else './lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from threading import Timer

two_hand_data = ""
two_hand_connected = False

class TwoHandListener(Leap.Listener):

    lPrevPalmX = rPrevPalmX = lPrevPalmY = rPrevPalmY = lPrevPalmZ = rPrevPalmZ = 0.0
    f=open("result.txt",'a')
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    # def on_init(self, controller):
    #     print "Initialized"

    def on_connect(self, controller):
        global two_hand_connected
        two_hand_connected = True
        # print "Connected"

    # def on_disconnect(self, controller):
    #     # Note: not dispatched when running in a debugger.
    #     print "Disconnected"

    # def on_exit(self, controller):
    #     self.f.write('\n')
    #     print "Exited"
        

    def on_frame(self, controller):

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

        if leftExist and rightExist:
            list = []

            for hand in frame.hands:

                palmX = palmY = palmZ = 0.0

                if hand.is_left:
                    handType = "Left hand"

                    tempPalm = hand.palm_position
                    palmTotal = str(tempPalm).replace("(", "").replace(")", "")

                    palmX = float(palmTotal.split(',')[0])
                    palmY = float(palmTotal.split(',')[1])
                    palmZ = float(palmTotal.split(',')[2])

                    lPalmDist = math.sqrt(math.pow(palmX - self.lPrevPalmX, 2) + math.pow(palmY - self.lPrevPalmY, 2) + math.pow(palmZ - self.lPrevPalmZ, 2))
                    # print lPalmDist,
                    list.insert(0,lPalmDist)

                    self.lPrevPalmX = palmX
                    self.lPrevPalmY = palmY
                    self.lPrevPalmZ = palmZ

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
                    list.insert(1,direction.pitch * Leap.RAD_TO_DEG)
                    list.insert(2,normal.roll * Leap.RAD_TO_DEG)
                    list.insert(3,direction.yaw * Leap.RAD_TO_DEG)

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
                    list.insert(4,thumbToIndex)
                    list.insert(5,indexToMiddle)
                    list.insert(6,middleToRing)
                    list.insert(7,ringToPinky)

                    thumbToPalm = math.sqrt(math.pow(thumbX - palmX, 2) + math.pow(thumbY - palmY, 2) + math.pow(thumbZ - palmZ, 2))
                    indexToPalm = math.sqrt(math.pow(indexX - palmX, 2) + math.pow(indexY - palmY, 2) + math.pow(indexZ - palmZ, 2))
                    middleToPalm = math.sqrt(math.pow(middleX - palmX, 2) + math.pow(middleY - palmY, 2) + math.pow(middleZ - palmZ, 2))
                    ringToPalm = math.sqrt(math.pow(ringX - palmX, 2) + math.pow(ringY - palmY, 2) + math.pow(ringZ - palmZ, 2))
                    pinkyToPalm = math.sqrt(math.pow(pinkyX - palmX, 2) + math.pow(pinkyY - palmY, 2) + math.pow(pinkyZ - palmZ, 2))
                    # print "thumbToPalm : %f, indexToPalm : %f, middleToPalm : %f, ringToPalm : %f, pinkyToPalm : %f" % (thumbToPalm, indexToPalm, middleToPalm, ringToPalm, pinkyToPalm),
                    list.insert(8,thumbToPalm)
                    list.insert(9,indexToPalm)
                    list.insert(10,middleToPalm)
                    list.insert(11,ringToPalm)
                    list.insert(12,pinkyToPalm)


                else:
                    handType = "Right hand"

                    tempPalm = hand.palm_position
                    palmTotal = str(tempPalm).replace("(", "").replace(")", "")

                    palmX = float(palmTotal.split(',')[0])
                    palmY = float(palmTotal.split(',')[1])
                    palmZ = float(palmTotal.split(',')[2])

                    rPalmDist = math.sqrt(math.pow(palmX - self.rPrevPalmX, 2) + math.pow(palmY - self.rPrevPalmY, 2) + math.pow(palmZ - self.rPrevPalmZ, 2))
                    # print "rPalmDist : %f" % (rPalmDist),
                    list.insert(13,rPalmDist)

                    self.rPrevPalmX = palmX
                    self.rPrevPalmY = palmY
                    self.rPrevPalmZ = palmZ

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
                # print i,
                data = ("%f " % i)
                self.f.write(data)

def remove_listener(controller, listener):
    global two_hand_data
    controller.remove_listener(listener)
    f = open("result.txt", 'r')
    two_hand_data = f.readline()
    f.close()

def main():
    global two_hand_connected
    # Create a sample listener and controller
    listener = TwoHandListener()
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # confirm whether two hands are connected
    while True:
        if two_hand_connected == False:
            # print "reconnecting"
            controller.remove_listener(listener)
            controller.add_listener(listener)
        elif two_hand_connected:
            break

    # after 6 seconds call remove_listner (extract data for 6 seconds)
    # print "timer start"
    t = Timer(6.0, remove_listener, args=[controller, listener])
    t.start()

if __name__ == "__main__":
    main()
