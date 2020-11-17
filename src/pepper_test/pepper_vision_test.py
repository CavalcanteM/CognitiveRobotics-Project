#!/usr/bin/python
import rospy
from naoqi_driver.naoqi_node import NaoqiNode
from pepper_test.srv import Shot
from pepper_test.srv import ShotResponse
from sensor_msgs.msg import Image

class Vision(NaoqiNode):
    def __init__(self):
        NaoqiNode.__init__(self,'pepper_vision')
        self.nameId = None
        self.connectNaoQi()
        self.pub_img = rospy.Publisher("take_image_topic", detector_msg, queue_size=3)
        pass

    def connectNaoQi(self):
        self.vision=self.get_proxy("ALVideoDevice")
        if self.vision is None:
            exit(1)
        kTopCamera = 0
        resolution = 1
        framerate = 5
        color_space = 11
        self.nameId = self.vision.subscribeCamera("pepper_rgb_camera", kTopCamera, resolution, color_space, framerate)
        rospy.loginfo('Using camera: rgb camera. Subscriber name is %s .' % (self.nameId))
        self.s = rospy.Service('pepper_vision_service', Shot, self.shot)

    def shot(self, data=None):
        img_to_send = Image()
        image = self.vision.getImageRemote(self.nameId)
        img_to_send.header.stamp = rospy.Time.now()
        img_to_send.height = image[1]
        img_to_send.width = image[0]
        layers = image[2] #3 for RGB
        img_to_send.encoding = "8UC3" #8 unsigned bit 3 channel
        img_to_send.step = img_to_send.width * layers
        img_to_send.data = image[6]
        self.pub_img.publish(img_to_send)
        rospy.loginfo('Sending image...')

        return ShotResponse(img_to_send)
        
if __name__=="__main__":
    vision_node = Vision()
    rospy.spin()


