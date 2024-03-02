from djitellopy import Tello
import cv2
import numpy as np
from FunctionsV2 import *
from time import sleep
from tof import TofTelloDrone
from moving_average import MovingAverage

RED_MODE = True
GREEN_MODE = True   
BLUE_MODE_1 = True
BLUE_MODE_2 = True
RED_QR_MODE = True
GREEN_QR_MODE = True
BLUE_QR_MODE = True
GO_BACK = True

n=1
green_range_low = np.array([40, 40, 40])
green_range_high = np.array([90, 255, 255])

tello = Tello()
det = cv2.QRCodeDetector()
tello.connect()

tello.takeoff()
sleep(6)
tello.rotate_clockwise(180)
sleep(3)
tello.move_forward(20)
sleep(1)
tello.move_up(20)
sleep(1)
tello.streamon()
sleep(1)
frame_read = tello.get_frame_read()
# create a named window
mode=True
go_back_init=True
while True:
    # read the frame from Tello
    frame = frame_read.frame
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # print("\n",RED_MODE,RED_QR_MODE,GREEN_MODE,GREEN_QR_MODE,BLUE_MODE_1,BLUE_MODE_2,BLUE_QR_MODE,"\n")
    print("\n",RED_MODE,RED_QR_MODE,GREEN_MODE,GREEN_QR_MODE,BLUE_MODE_1,BLUE_MODE_2,BLUE_QR_MODE,"\n")
    # _,_,found_blue,frame_image = ColorThreshold(frame)
    # found_blue_triangle,original_image,is_tri = FindTriangle(found_blue,frame_image)
    # # display the frame
    # cv2.imshow("Tello Camera", original_image)
    # cv2.imshow("Red",found_blue_triangle)

    # quit the program if 'q' is pressed 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        # ++++++++++++Add Mission below+++++++++++++++++#
    if (RED_MODE == True) & (RED_QR_MODE == True):
        found_red,_,_,original_image = ColorThreshold(frame)
        found_red_circle,red_circle_detect, is_circle,red_center = FindCircle(found_red,original_image)
        # display the frame
        cv2.imshow("Tello Camera", red_circle_detect)
        tello.send_rc_control(0,0,0,30) # clockwise
        # print("turn")
        if is_circle is True:
            cv2.imwrite("red_circle.png",red_circle_detect)
            print("\n\n\nFront\n\n\n")
            cv2.destroyAllWindows()
            tello.move_down(20)
            sleep(1)
            RED_MODE = False
    elif (RED_MODE == False) & (RED_QR_MODE == True):
        qr_image,qr_info,is_qr = QRCode(det,frame)
        print(qr_info)
        tello.send_rc_control(0,0,0,30)
        cv2.imshow("QR",qr_image)
        if is_qr == True:
            print("QR stop")
            cv2.imwrite("red_qr.png",qr_image)
            tello.move_up(20)
            sleep(1)
            cv2.destroyAllWindows()
            RED_QR_MODE = False
    elif (RED_QR_MODE == False) & (GREEN_MODE == True) & (GREEN_QR_MODE == True):
        tello.send_rc_control(0,0,0,30) # clockwise
        hsv_frame = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
        green_mask = cv2.inRange(hsv_frame, green_range_low, green_range_high)
        # _,_,found_green,original_image = ColorThreshold(frame)
        # found_green_circle,green_circle_detect, is_circle,green_center = FindCircle(found_green,original_image)
        green_canny = CannyColor(green_mask)
        found_green_circle,green_circle_detect, is_circle,green_center = FindCircle(green_canny,frame)
        cv2.imshow(")",green_canny)
        cv2.imshow("Tello Camera", green_circle_detect)
        if is_circle == True:
            cv2.imwrite("green_circle.png",green_circle_detect)
            print("\n\n\nFront\n\n\n")
            cv2.destroyAllWindows()
            tello.move_down(20)
            sleep(1)
            GREEN_MODE = False

    elif (RED_QR_MODE == False) & (GREEN_MODE == False) & (GREEN_QR_MODE == True):
        qr_image,qr_info,is_qr = QRCode(det,frame)
        print(qr_info)
        tello.send_rc_control(0,0,0,30)
        cv2.imshow("QR",qr_image)
        if is_qr == True:
            print("QR stop")
            cv2.imwrite("green_qr.png",qr_image)
            tello.move_up(30)
            sleep(1)
            # tello.rotate_counter_clockwise(20)
            #sleep(1)
            #tello.move_forward(50)
            #sleep(1)
            cv2.destroyAllWindows()
            GREEN_QR_MODE = False
    elif (GREEN_QR_MODE == False) & (BLUE_MODE_1 == True) & (BLUE_MODE_2 == True) & (BLUE_QR_MODE == True):
        tello.send_rc_control(0,0,0,30) # clockwise
        _,_,found_blue,original_image = ColorThreshold(frame)
        found_blue_triangle,blue_triangle_detect, is_triangle,tri_center = FindTriangle(found_blue,original_image)
        cv2.imshow("Tello Camera", blue_triangle_detect)
        if is_triangle == True:
            # tof = TofTelloDrone(tello)
            # tof.start()
            # #tof_moving_average = MovingAverage(5)

            print("\n\n\nBack\n\n\n")
            cv2.imwrite("blue_triangle.png",blue_triangle_detect)
            # Update the moving average with the new ToF number
            #tof_moving_average.add(Tof_num)
            # Use the average ToF number in your decision logic
            #Tof_num_average = tof_moving_average.average()
            BLUE_MODE_1 = False
    elif (GO_BACK == True) & (BLUE_MODE_1 == False) & (BLUE_MODE_2 == True) & (BLUE_QR_MODE == True):
            if go_back_init == True:
                tello.move_up(50)
                sleep(1)
                tello.rotate_clockwise(20)
                go_back_init = False
                sleep(3)
                continue
            # tof = TofTelloDrone(tello)
            # tof.start()
            # Tof_num = tof.get_tof()
            # sleep(1)
            # if n<5:
            #     tello.move_forward(40)
            #     n += 1
            #     print("#################################move_forward")
            #     # Add area control code for distance measurement
            #     print(Tof_num,'\n')
            # else:
            #     tello.move_forward(40)
                # sleep(1)
                # print("move over the box")
                # print(Tof_num,'\n')
                # print("you are now over the box")
            tello.move_forward(160)
            sleep(3)
            tello.move_down(60)
            sleep(1)
            GO_BACK = False
            #     #tello.hover()
    elif (GO_BACK == False) & (BLUE_MODE_1 == False) & (BLUE_MODE_2 == True) & (BLUE_QR_MODE == True):
        tello.send_rc_control(0,0,0,30) # clockwise
        _,_,found_blue,original_image = ColorThreshold(frame)
        found_blue_circle,blue_circle_detect, is_circle,blue_center = FindCircle(found_blue,original_image)
        cv2.imshow("Tello Camera", blue_circle_detect)
        if is_circle == True:
            tello.rotate_clockwise(10)
            # cv2.imwrite("blue_circle.png",blue_circle_detect)
            sleep(3)
            tello.move_back(20)
            sleep(1)
            print("\n\n\nFront\n\n\n")
            cv2.imwrite("blue_circle.png",blue_circle_detect)
            cv2.destroyAllWindows()
            tello.move_down(35)
            sleep(1)
            BLUE_MODE_2 = False

    elif (BLUE_MODE_1 == False) & (BLUE_MODE_2 == False) & (BLUE_QR_MODE == True):
        qr_image,qr_info,is_qr = QRCode(det,frame)
        print(qr_info)
        tello.send_rc_control(0,0,0,30)
        cv2.imshow("QR",qr_image)
        if is_qr == True:
            print("QR stop")
            cv2.imwrite("blue_qr.png",qr_image)
            # tello.move_up(20)
            # sleep(1)
            cv2.destroyAllWindows()
            BLUE_QR_MODE = False
            break
    
tello.land()
tello.streamoff()