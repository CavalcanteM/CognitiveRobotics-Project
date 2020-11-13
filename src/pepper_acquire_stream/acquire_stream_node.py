#!/usr/bin/env python
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rospy
from std_msgs.msg import Bool
from std_msgs.msg import String

class StreamController:
    def __init__(self):
        self.br = CvBridge()
        self.pub_img = rospy.Publisher("take_image_topic", Image, queue_size=3)
        self.pub_head_node = rospy.Publisher("head_movement_start", String, queue_size=0)
        self.sub = rospy.Subscriber("head_movement_done", Bool, self.callback)        
        self.count = 0

    def callback(self, msg):
        if msg.data and self.count < 3:
            self.take_frame()
            
    def take_frame(self):
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        cap.release()
        next_position = self.head_position_update()
        self.pub_img.publish(self.br.cv2_to_imgmsg(frame))
        self.pub_head_node.publish(next_position)

    def head_position_update(self):
        self.count += 1
        if self.count == 1:
            return "left"
        elif self.count == 2:
            return "right"
        elif self.count == 3:
            return "reset"

if __name__ == "__main__":
    rospy.init_node('stream_acquire')
    stream_controller = StreamController()
    stream_controller.take_frame()
    rospy.spin()