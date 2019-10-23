#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

bridge = CvBridge()
video_capture1 = cv2.VideoCapture('catkin_ws/src/ball_tracker/src/video/tennis-ball-video.mp4')


def OpenVideo():
	#video_capture1 = cv2.VideoCapture(0)
	Test = False
	if video_capture1.isOpened():
		print 'it is opened successfully!'
		Test = True
	else:
		print 'cannot open it!'
	return Test


def main():
	Test = OpenVideo()

	pub = rospy.Publisher("image_topic_2",Image)

	rospy.init_node('tennis_ball_publisher', anonymous=True)
	rate = rospy.Rate(1)


	while(Test):
		ret, frame = video_capture1.read()
		cv2.imshow("Frame",frame)

		# add your file here
		frame_ros = bridge.cv2_to_imgmsg(frame, "bgr8")
		pub.publish(frame_ros)


		if cv2.waitKey(100) & 0xFF == ord('q'):
			break



	
	video_capture1.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
    main()




    '''
		try:
			frame_ros = bridge.cv2_to_imgmsg(frame, "bgr8")
      		pub.publish(frame_ros)
    	except CvBridgeError as e:
      		print(e)
      		'''
		#if cv2.waitKey(100) & 0xFF == ord('q'):
		#	break





'''

	while(Test):
		ret, frame = video_capture1.read()
		#print type(frame)
		#frame_ros = bridge.cv2_to_imgmsg(frame, "bgr8")
      	#pub.publish(frame_ros)
      	cv2.imshow("Frame",frame)
      	if cv2.waitKey(100) & 0xFF == ord('q'):
      		break

'''	

