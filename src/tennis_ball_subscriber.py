#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import numpy as np

bridge = CvBridge()

def Color_Mask(frame):
  frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  yellowLower =(30, 150, 100)
  yellowUpper = (50, 255, 255)
  frame_mask = cv2.inRange(frame_hsv, yellowLower, yellowUpper)

  return frame_mask

def getContours(binary_image):      
    _, contours, hierarchy = cv2.findContours(binary_image, 
                                              cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_contours(image, contours):
    index = -1 #means all contours
    thickness = 4 #thinkess of the contour line
    color = (255, 0, 255) #color of the contour line
    cv2.drawContours(image, contours, index, color, thickness)
    return image
    #cv2.imshow(image_name,image)




def process_contours(binary_image, rgb_image, contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    
    for c in contours:
        area = cv2.contourArea(c)
        if area > 250:
          perimeter= cv2.arcLength(c, True)
          ((x, y), radius) = cv2.minEnclosingCircle(c)
          cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
          cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
          cx, cy = get_contour_center(c)
          cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
          cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
          print ("Area: {}, Perimeter: {}".format(area, perimeter))
    print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)


def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy




def image_callback(ros_image):
  print 'got a frame'
  global bridge
  #convert ros_image into an opencv-compatible image
  try:
    frame = bridge.imgmsg_to_cv2(ros_image, "bgr8")
  except CvBridgeError as e:
      print(e)

  #from now on, you can work exactly like with opencv
  frame_mask = Color_Mask(frame) 
  contours_in_frame = getContours(frame_mask)
  frame_contours = draw_contours(frame_mask , contours_in_frame)  
  process_contours(frame_mask, frame, contours_in_frame)
  cv2.imshow("Frame",frame_contours)
  cv2.waitKey(100)

  #from now on, you can work exactly like with opencv

  #(rows,cols,channels) = cv_image.shape
  #if cols > 200 and rows > 200 :
  #    cv2.circle(cv_image, (100,100),90, 255)
  #font = cv2.FONT_HERSHEY_SIMPLEX
  #cv2.putText(cv_image,'Webcam Activated with ROS & OpenCV!',(10,350), font, 1,(255,255,255),2,cv2.LINE_AA)
  #cv2.imshow("Image window", cv_image)
  #cv2.waitKey(3)

  
def main(args):
  rospy.init_node('image_subscriber', anonymous=True)
  #for turtlebot3 waffle
  #image_topic="/camera/rgb/image_raw/compressed"
  #for usb cam
  #image_topic="/usb_cam/image_raw"
  image_sub = rospy.Subscriber("image_topic_2",Image, image_callback)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)