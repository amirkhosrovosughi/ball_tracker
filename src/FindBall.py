#!/usr/bin/env python 

import cv2
import numpy as np



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






def main():
	Test = OpenVideo()
	while(Test):
		ret, frame = video_capture1.read()

		frame_mask = Color_Mask(frame) 
		contours_in_frame = getContours(frame_mask)

		'''
		i = 0
		for value in contours_in_frame:
			print i
			i = i + 1
		'''
		frame_contours = draw_contours(frame_mask , contours_in_frame)

		
		process_contours(frame_mask, frame, contours_in_frame)



		cv2.imshow("Frame",frame_contours)
		if cv2.waitKey(100) & 0xFF == ord('q'):
			break


	video_capture1.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
    main()