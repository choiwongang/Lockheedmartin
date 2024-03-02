from djitellopy import Tello
import cv2
from time import sleep
import numpy as np
from FunctionsV3 import *
from PID_9_4 import *
import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression
from initialize2 import * 
from searching4 import *
from searching4_2 import *

# Mission Start
MISSION = True

# Initial mode
INIT = True

# Landing mode
LAND = False

# Drone Side State
LEFT = False
MID = True
RIGHT = False

# detection mode

DET = 1
NUMBER = True
RING = False
FIRST_TAKE = 0
# PID control mode
PID = False 

# YOLO
model = attempt_load('models/best.pt')
model.eval()
model.cuda()

# Parameter Initialization
used_number = []

motion = 60      # cm
motion_1 = 80
right_side = 0   # [-2 2]
left_side = 0    # [-2 2]
flag = 0         # 0 : right move / 1 : left move

sequence_idx = 0 # [0 3]

count = 0        # imwrite counting

prev_color_idx = 0
color_idx = 0    # red : 0 / green : 1 / blue : 2

# pid mode
pid1 = False
pid2 = False
TO_Second_PID = False
Bang = False
Second_PID = False
centered_counter=0

def FindSequence(sequence):
    sequence = np.sort(sequence)

    common_difference = sequence[1] - sequence[0]
    
    next_number = sequence[2] + common_difference
    
    # 만약 10의 자리를 넘어가면, 1의 자리만 사용
    if next_number >= 10:
        next_number = next_number % 10
    
    # 새로운 수를 배열에 추가
    sequence = np.append(sequence,next_number)
    
    return sequence
# Start-----------------------------------------------

tello = Tello()

tello.connect()
tello.takeoff()
sleep(5)

tello.streamon()
frame_read = tello.get_frame_read()

tello.move_forward(80)
sleep(2)

while MISSION:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame = frame_read.frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame,(640,480))
    
    if (INIT == True) and (FIRST_TAKE == 0):
        p1,p2,cx,cy,numbers,is_num,frame = detect_and_draw_boxes_init(frame,model)
        if len(numbers) != 0:
            for num in numbers:
                if num not in used_number:
                    used_number = np.append(used_number, num)
                    used_number = np.sort(used_number)
    
        tello.move_right(120)
        sleep(6)
        FIRST_TAKE += 1
    elif (INIT == True) and (FIRST_TAKE == 1):
        p1,p2,cx,cy,numbers,is_num,frame = detect_and_draw_boxes_init(frame,model)
        if len(numbers) != 0:
            for num in numbers:
                if num not in used_number:
                    used_number = np.append(used_number, num)
                    used_number = np.sort(used_number)
    
        tello.move_left(250)
        sleep(6)
        FIRST_TAKE += 1
    elif (INIT == True) and (FIRST_TAKE == 2):
        p1,p2,cx,cy,numbers,is_num,frame = detect_and_draw_boxes_init(frame,model)
        if len(numbers) != 0:
            for num in numbers:
                if num not in used_number:
                    used_number = np.append(used_number, num)
                    used_number = np.sort(used_number)
        
        if len(used_number) == 3:
            used_number = FindSequence(used_number)
            print("Get Sequence!!!!\n",used_number)
            tello.move_right(120)
            sleep(6)
            INIT = False
            continue
        else:
            FIRST_TAKE = 0
            tello.move_right(120)
            sleep(6)

    elif (INIT == False) and (NUMBER == True) and (PID == False) and (RING == False) :
        print(used_number)
        print("rigt side : ",right_side," left side : ",left_side, " flag : ",flag)
        if   (right_side == 0) and (left_side == 0) and (flag == 0):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                #cv2.imshow("Number Detection",frame)
                # cv2.line(frame, (80, 0), (80, 480), (255, 255, 0), 3)
                # cv2.line(frame, (560, 0), (560, 480), (255, 255, 0), 3)
                if (is_num) and (center_x >= 80) and (center_x <= 560):
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(1)
                tello.move_right(motion)
                sleep(3)
                right_side +=1
        elif (right_side == 1) and (left_side == 0) and (flag == 0):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(1)
                tello.move_right(motion)
                sleep(3)
                right_side +=1
        elif (right_side == 2) and (left_side == 0) and (flag == 0):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(3)
                flag = 1  
        elif (right_side == 2) and (left_side == 0) and (flag == 1):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                tello.move_left(motion)
                sleep(3)
                right_side -= 1
        elif (right_side == 1) and (left_side == 0) and (flag == 1):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                tello.move_left(motion)
                sleep(3)
                right_side -= 1
        elif (right_side == 0) and (left_side == 0) and (flag == 1):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                #cv2.imshow("Number Detection",frame)
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                tello.move_left(motion)
                sleep(3)
                left_side += 1
        elif (right_side == 0) and (left_side == 1) and (flag == 1):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                #cv2.imshow("Number Detection",frame)
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(1)
                tello.move_left(motion)
                sleep(3)
                left_side += 1
        elif (right_side == 0) and (left_side == 2) and (flag == 1):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                #cv2.imshow("Number Detection",frame)
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(1)
                flag = 0
        elif (right_side == 0) and (left_side == 2) and (flag == 0):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                #cv2.imshow("Number Detection",frame)
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx +=1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(1)
                tello.move_right(motion)
                sleep(3)
                left_side -= 1
        elif (right_side == 0) and (left_side == 1) and (flag == 0):
                p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[sequence_idx])
                #cv2.imshow("Number Detection",frame)
                if is_num:
                    cv2.imwrite(f"result/sequence_number_{count}.png",frame)
                    count += 1
                    #  sequence_idx-1 = sequence_idx # store previous index
                    sequence_idx += 1 # update next sequence
                    NUMBER = False
                    PID = True                    
                    # cv2.destroyAllWindows()
                    continue
                sleep(1)
                tello.move_right(motion)
                sleep(3)
                left_side -= 1                     
    
    elif (INIT == False) and (NUMBER == False) and (PID == True) and (RING == False) and (DET == 1):
        print("PID PHASE")
        p1,p2, center_x,center_y,is_num,frame = detect_and_draw_boxes(frame, model,used_number[ sequence_idx-1])
        #add PID control here     
        if is_num:
            TO_Second_PID,centered_counter = Pid_first_phase(p1,p2, tello,center_x,center_y,centered_counter)
            print("I am looking at the Number##################")
            #frame=draw_guidelines(frame)
            #cv2.imshow('processed',frame)
            #cv2.imshow('green',frame)
            if TO_Second_PID:
                Second_PID = True    

            if Second_PID:
                if (p1 != (0,0)) and (p2 != (0,0)) :
                    Bang = Pid_second_phase(p1,p2,tello,center_x,center_y)
                else:
                    tello.send_rc_control(0,0,0,0)
                    time.sleep(0.05)
                if Bang:
                    #Done,centered_counter,frame=Ring(found_green,frame,tello,centered_counter)
                    #if Done:
                        print("PID finished")
                        tello.move_forward(230)
                        sleep(5)
                        print("right_side:")
                        print(right_side)
                        print("left_side:")
                        print(left_side)
                        
                        if (right_side == 0) and (left_side == 0):
                            print("mid")
                            tello.rotate_clockwise(180)
                            sleep(3)
                            #continue
                        elif (right_side == 1) and (left_side == 0):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 1) and (left_side == 0)")
                            tello.move_left(motion)
                            right_side -= 1
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            # continue
                        elif (right_side == 2) and (left_side == 0):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 2) and (left_side == 0)")
                            tello.move_left(motion*2)
                            right_side -= 2
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            # continue
                        elif (right_side == 0) and (left_side == 1):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 0) and (left_side == 1)")
                            tello.move_right(motion)
                            left_side -= 1
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            # continue
                        elif (right_side == 0) and (left_side == 2):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 0) and (left_side == 2)")
                            tello.move_right(motion*2)
                            left_side -= 2
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            # continue
                        # right_side = 0
                        # left_side = 0
                        PID = False
                        RING = True
                        Second_PID = False
                        DET = -1
                        continue #++++

    elif (INIT == False) and (NUMBER == False) and (PID == False) and (RING == True):
        found_red,found_green,found_blue,frame = ColorThreshold(frame)
        if color_idx == 0:
            canny_image = found_red
            #continue
        elif color_idx == 1:
            canny_image = found_green 
            #continue  
        elif color_idx == 2:
            canny_image = found_blue
            #continue
        print(color_idx)
        if     (right_side == 0) and (left_side == 0) and (flag == 0):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_right(motion)
            sleep(3)
            right_side +=1
        elif   (right_side == 1) and (left_side == 0) and (flag == 0):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_right(motion)
            sleep(3)
            right_side +=1
        elif   (right_side == 2) and (left_side == 0) and (flag == 0):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            flag = 1
        elif   (right_side == 2) and (left_side == 0) and (flag == 1):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_left(motion)
            sleep(3)
            right_side -= 1
        elif   (right_side == 1) and (left_side == 0) and (flag == 1):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_left(motion)
            sleep(3)
            right_side -= 1
        elif   (right_side == 0) and (left_side == 0) and (flag == 1):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_left(motion)
            sleep(3)
            left_side += 1
        elif   (right_side == 0) and (left_side == 1) and (flag == 1):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_left(motion)
            sleep(3)
            left_side += 1
        elif   (right_side == 0) and (left_side == 2) and (flag == 1):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_right(motion)
            sleep(3)
            left_side -= 1
            flag = 0
        elif   (right_side == 0) and (left_side == 2) and (flag == 0):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_right(motion)
            sleep(3)
            left_side -= 1
        elif   (right_side == 0) and (left_side == 1) and (flag == 0):
            _,frame,is_rec,_ = FindRectangle(canny_image,frame,color_idx)
            #cv2.imshow("Number Detection",frame)
            if is_rec:
                cv2.imwrite(f"result/color_{count}.png",frame)
                count += 1
                # prev_color_idx = color_idx # store previous index
                # color_idx +=1 # update next sequence
                RING = False
                PID = True                    
                # cv2.destroyAllWindows()
                continue
            sleep(1)
            tello.move_right(motion)
            sleep(3)
            left_side -= 1

    elif (INIT == False) and (NUMBER == False) and (PID == True) and (RING == False) and (DET == -1):
        found_red,found_green,found_blue,frame = ColorThreshold(frame)
        if color_idx == 0:
            canny_image = found_red
            #continue
        elif color_idx == 1:
            canny_image = found_green 
            #continue  
        elif color_idx == 2:
            canny_image = found_blue
            #continue
        p1,p2, center_x,center_y,frame = Ring1(canny_image,frame)
        #add PID control here
        if is_num:
            TO_Second_PID,centered_counter = Pid_first_phase(p1,p2, tello,center_x,center_y,centered_counter)
            print("I am looking at the Number##################")
            #frame=draw_guidelines(frame)
            #cv2.imshow('processed',frame)
            #cv2.imshow('green',frame)
            if TO_Second_PID:
                Second_PID = True    

            if Second_PID:
                #frame=draw_guidelines(frame)
                #cv2.imshow('processed',frame)
                #cv2.imshow('green',frame)
                if (p1 != 0) and (p2 != 0) :
                    Bang = Pid_second_phase2(p1,p2,tello,center_x,center_y)
                else:
                    tello.send_rc_control(0,0,0,0)
                    time.sleep(0.05)
                if Bang:
                    #Done,centered_counter,frame=Ring(found_green,frame,tello,centered_counter)
                    #if Done:
                        print("PID finished")
                        tello.move_forward(230)
                        sleep(5)
                        if (right_side == 0) and (left_side == 0):
                            print("mid")
                            tello.rotate_clockwise(180)
                            sleep(3)
                            #continue
                        elif (right_side == 1) and (left_side == 0):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 1) and (left_side == 0)")
                            tello.move_left(motion)
                            right_side -= 1
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            #continue
                        elif (right_side == 2) and (left_side == 0):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 2) and (left_side == 0)")
                            tello.move_left(motion*2)
                            right_side -= 2
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            #continue
                        elif (right_side == 0) and (left_side == 1):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 0) and (left_side == 1)")
                            tello.move_right(motion)
                            left_side -= 1
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            #continue 
                        elif (right_side == 0) and (left_side == 2):
                            print("right_side:")
                            print(right_side)
                            print("left_side:")
                            print(left_side)
                            print("(right_side == 0) and (left_side == 2)")
                            tello.move_right(motion*2)
                            left_side -= 2
                            sleep(3)
                            tello.rotate_clockwise(180)
                            sleep(3)
                            #continue
                        # right_side = 0
                        # left_side = 0
                        PID = False
                        NUMBER = True
                        DET = 1
                        color_idx +=1
                        Second_PID = False
                        continue
    
    # elif LAND:
    #     # Use used_number[3] for landing
    #     if     (right_side == 0) and (left_side == 0) and (flag == 0):
    #     elif   (right_side == 1) and (left_side == 0) and (flag == 0):
    #     elif   (right_side == 2) and (left_side == 0) and (flag == 0):
    #     elif   (right_side == 0) and (left_side == 0) and (flag == 1):
    #     elif   (right_side == 1) and (left_side == 0) and (flag == 1):
    #     elif   (right_side == 2) and (left_side == 0) and (flag == 1):
    #     elif   (right_side == 0) and (left_side == 1) and (flag == 0):
    #     elif   (right_side == 0) and (left_side == 2) and (flag == 0):
    #     elif   (right_side == 0) and (left_side == 1) and (flag == 1):
    #     elif   (right_side == 0) and (left_side == 2) and (flag == 1):
    cv2.imshow("frame",frame)
#tello.streamoff()
#cv2.destroyAllWindows()