# from sympy import Symbol, solve
import numpy as np
# import sympy
from djitellopy import Tello
import cv2
from FunctionsV3 import *
import time

import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression

#from tof import TofTelloDrone
#from moving_average import MovingAverage

frameWidth = 640
frameHeight = 480
deadZone =30
deadZone2=12
# from sympy import Symbol, solve
import numpy as np
# import sympy

def Rotation_MAT(yaw,pitch,roll):
    f32Yaw_rad=yaw
    f32Pitch_rad=pitch
    f32Roll_rad=roll

    tDCM_Yaw_Mat =np.matrix(([np.cos(f32Yaw_rad),-np.sin(f32Yaw_rad),0],
                            [np.sin(f32Yaw_rad),np.cos(f32Yaw_rad), 0],
                            [0,0,1]))

    tDCM_Pitch_Mat = np.matrix([[np.cos(f32Pitch_rad), 0, np.sin(f32Pitch_rad)],
                                [0,1,0],
                                [-np.sin(f32Pitch_rad), 0, np.cos(f32Pitch_rad)]])

    tDCM_Roll_Mat = np.matrix([[1,0,0],
                                [0,np.cos(f32Roll_rad),-np.sin(f32Roll_rad)],
                                [0,np.sin(f32Roll_rad),np.cos(f32Roll_rad)]])

    tRotation_mat = tDCM_Yaw_Mat * tDCM_Pitch_Mat * tDCM_Roll_Mat
    return tRotation_mat

def Transformation_MAT(rotation, position):
    transform_mat= np.mat([[rotation[0,0],rotation[0,1],rotation[0,2],position[0,0]],
                            [rotation[1,0],rotation[1,1],rotation[1,2],position[1,0]],
                            [rotation[2,0],rotation[2,1],rotation[2,2],position[2,0]],
                            [0,0,0,1]])
    return transform_mat

def Pos_vec_from_inertia(Altitude, yaw, pixel_value):
    ##input unit##
    # Altitude for cm
    # yaw for deg
    # pixel value is no
    # malized in range of 0 ~ 2000
    
    ### init status ###
    f32DroneXposition_m = 0
    f32DroneYposition_m = 0
    f32DroneAltitude_m = Altitude*0.01
    f32DroneYaw_rad = 0
    f32DronePitch_rad = (-6.8)*np.pi/180
    f32DroneRoll_rad = yaw*np.pi/180
    f32GimbalYaw_rad =0
    f32GimbalPitch_rad =0
    f32GimbalRoll_rad=0

    #0~2000 사이의 정규화된 픽셀좌표
    f32PixelsX_normalized =pixel_value[0]
    f32PixelsY_normalized =pixel_value[1]

    f32PixelsXposition = f32PixelsX_normalized * 1.2721944218759018e+03 * 0.001 
    f32PixelsYposition = f32PixelsY_normalized * 9.3756914021851821e+02 * 0.001

    f32Position_Inertia2Body = np.array([[f32DroneXposition_m],[f32DroneYposition_m],[-f32DroneAltitude_m]])
    f32Position_Body2Gimbal = np.array([[0], [0], [0]])
    f32Position_Gimbal2Camera = np.array([[0], [0], [0]])

    tRotation_Inertia2Body = Rotation_MAT(f32DroneYaw_rad,f32DronePitch_rad,f32DroneRoll_rad)
    tRotation_Body2Gimbal = Rotation_MAT(f32GimbalYaw_rad,f32GimbalPitch_rad,f32GimbalRoll_rad)
    tRotation_Gimbal2Camera =np.mat([[0, 0, 1],
                                    [0, 1, 0],
                                    [-1, 0, 0]])

    tTransformation_Inertia2Body = Transformation_MAT(tRotation_Inertia2Body,f32Position_Inertia2Body)
    tTransformation_body2gimbal = Transformation_MAT(tRotation_Body2Gimbal,f32Position_Body2Gimbal)
    tTransformation_Gimbal2Camera = Transformation_MAT(tRotation_Gimbal2Camera,f32Position_Gimbal2Camera)

    C_matrix_ocv = np.mat([ [ 1.8916555691187248e+03, 0., 1.2721944218759018e+03], [0.,
       1.9012817024374301e+03, 9.3756914021851821e+02], [0., 0., 1. ]]); 


    f32Position_ObjBar_from_Camera_ocv= (np.linalg.inv(C_matrix_ocv))*np.array([[f32PixelsXposition], [f32PixelsYposition], [1]])
    f32Position_ObjBar_from_Camera = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) * f32Position_ObjBar_from_Camera_ocv
    f32Position_ObjBar_from_Camera =np.append(f32Position_ObjBar_from_Camera, np.array([[1]]), axis=0)

    tTransform_I2C =  tTransformation_Inertia2Body * tTransformation_body2gimbal * tTransformation_Gimbal2Camera

    f32Position_ObjBar_from_Inertia = tTransform_I2C * f32Position_ObjBar_from_Camera
    f32Position_CC_from_Inertia = (tTransform_I2C) * np.array([[0], [0], [0], [1]])
    print(f32Position_CC_from_Inertia[2,0])
    f32Lambda = (f32Position_CC_from_Inertia[2,0] + 0.7 ) / ((f32Position_CC_from_Inertia[2,0])-f32Position_ObjBar_from_Inertia[2,0])
    f32Position_Obj_from_Inertia = f32Position_CC_from_Inertia + f32Lambda * (f32Position_ObjBar_from_Inertia - f32Position_CC_from_Inertia);
    return f32Position_Obj_from_Inertia

def unit_vec_q_from_Body(pixel_value):
    ### init status ###
    # f32DroneXposition_m = Local_pos[0]
    # f32DroneYposition_m = Local_pos[1]
    # f32DroneAltitude_m = Local_pos[2]
    # f32DroneYaw_rad = Attitude[0]
    # f32DronePitch_rad = Attitude[1]
    # f32DroneRoll_rad = Attitude[2]
    f32GimbalYaw_rad =0
    f32GimbalPitch_rad = (-5)*np.pi/180
    f32GimbalRoll_rad=0

    #0~2000 사이의 정규화된 픽셀좌표
    f32PixelsX_normalized =pixel_value[0]
    f32PixelsY_normalized =pixel_value[1]

    f32PixelsXposition = f32PixelsX_normalized * 1.2721944218759018e+03 * 0.001 
    f32PixelsYposition = f32PixelsY_normalized * 9.3756914021851821e+02 * 0.001

    # f32Position_Inertia2Body = np.array([[f32DroneXposition_m],[f32DroneYposition_m],[-f32DroneAltitude_m]])
    f32Position_Body2Gimbal = np.array([[0], [0], [0]])
    f32Position_Gimbal2Camera = np.array([[0], [0], [0]])

    # tRotation_Inertia2Body = Rotation_MAT(f32DroneYaw_rad,f32DronePitch_rad,f32DroneRoll_rad)
    tRotation_Body2Gimbal = Rotation_MAT(f32GimbalYaw_rad,f32GimbalPitch_rad,f32GimbalRoll_rad)
    tRotation_Gimbal2Camera =np.mat([[0, 0, 1],
                                    [0, 1, 0],
                                    [-1, 0, 0]])

    # tTransformation_Inertia2Body = Transformation_MAT(tRotation_Inertia2Body,f32Position_Inertia2Body)
    tTransformation_body2gimbal = Transformation_MAT(tRotation_Body2Gimbal,f32Position_Body2Gimbal)
    tTransformation_Gimbal2Camera = Transformation_MAT(tRotation_Gimbal2Camera,f32Position_Gimbal2Camera)

    C_matrix_ocv = np.mat([ [ 1.8916555691187248e+03, 0., 1.2721944218759018e+03], [0.,
       1.9012817024374301e+03, 9.3756914021851821e+02], [0., 0., 1. ]]); 

    f32Position_ObjBar_from_Camera_ocv= (np.linalg.inv(C_matrix_ocv))*np.array([[f32PixelsXposition], [f32PixelsYposition], [1]])
    f32Position_ObjBar_from_Camera = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) * f32Position_ObjBar_from_Camera_ocv
    f32Position_ObjBar_from_Camera =np.append(f32Position_ObjBar_from_Camera, np.array([[1]]), axis=0)

    tTransform_B2C =  tTransformation_body2gimbal * tTransformation_Gimbal2Camera

    f32Position_ObjBar_from_Body = tTransform_B2C * f32Position_ObjBar_from_Camera
    q_vetor_form_Body = f32Position_ObjBar_from_Body
    return q_vetor_form_Body

def marker_location_from_body(upper_side_marker,lowwer_side_marker, real_length):
    """Find marker's local distance form Drone's Body coordinate"""
    p1 = unit_vec_q_from_Body(upper_side_marker)
    p2 = unit_vec_q_from_Body(lowwer_side_marker)
    print(f"upper : {upper_side_marker}\tlowwer : {lowwer_side_marker}")
    print(f"p1 : {p1}\t p2 : {p2}")
    # f32Lambda = 0.15 / ((p2[2,0])-p1[2,0])
    f32Lambda = real_length / ((p2[2,0])-p1[2,0])
    print("f32Lambda :", f32Lambda)
    center_of_marker = (p1+p2)*0.5*f32Lambda
    center_of_marker[3] = 0.0
    return center_of_marker


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def getDirection(boundingBox):
    pixel_up_left = boundingBox[0]
    pixel_down_left = boundingBox[1]
    pixel_up_right = boundingBox[2]
    pixel_center = np.array([1000,1000])


    q2 = np.array(unit_vec_q_from_Body(pixel_up_left))
    q2 = np.delete(q2,[3],0)
    q1 = np.array(unit_vec_q_from_Body(pixel_down_left))
    q1 = np.delete(q1,[3],0)
    q3 = np.array(unit_vec_q_from_Body(pixel_up_right))
    q3 = np.delete(q3,[3],0)
    q0 = np.array([[1],[0],[0]])

    if -q1[2,0] < -q0[2,0] and -q2[2,0] > -q0[2,0]:
        print('Hold Alt.')
    elif -q1[2,0] > -q0[2,0]:
        print('Alt up')
    elif -q2[2,0] < -q0[2,0]:
        print('Alt Down')

def Ring1(mask_image,original_image):
    contours, _ = cv2.findContours(mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    original_image=draw_guidelines(original_image)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10000:
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            objCorner = len(approx)
            pos_x, pos_y, w, h = cv2.boundingRect(approx)

            if objCorner == 4:
                p1=(pos_x,pos_y)
                p2=(pos_x+w,pos_y+h)
                M = cv2.moments(cnt)
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
                center = (x, y)

                cv2.drawContours(original_image, cnt, -1, (255, 255, 255), 3)
                cv2.circle(original_image, center, 5, (0, 0, 255), -1)
                text = f"Center: ({x}, {y})"
                cv2.putText(original_image, text, (x - 60, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if (p1 is not None) and (p2 is not None):
                    return p1,p2,x,y,original_image
    
    p1 = (0,0) #++++
    p2=  (0,0) #++++
    x=0
    y=0
    return p1,p2,x,y,original_image
    
    
def draw_guidelines(imgContour):
    # Drawing the guide lines on the frame
    cv2.line(imgContour, (int(frameWidth/2)-deadZone, 0), (int(frameWidth/2)-deadZone, frameHeight), (255, 255, 0), 3)
    cv2.line(imgContour, (int(frameWidth/2)+deadZone, 0), (int(frameWidth/2)+deadZone, frameHeight), (255, 255, 0), 3)
    cv2.line(imgContour, (0, int(frameHeight/2)-deadZone), (frameWidth, int(frameHeight/2)-deadZone), (255, 255, 0), 3)
    cv2.line(imgContour, (0, int(frameHeight/2)+deadZone), (frameWidth, int(frameHeight/2)+deadZone), (255, 255, 0), 3)
    
    cv2.circle(imgContour, (int(frameWidth/2), int(frameHeight/2)), 5, (0, 0, 255), 5)
    return imgContour

def Pid_first_phase(p1,p2, tello,cx,cy,centered_counter):
    """ Move drone to First Flag position
    color_marker_pixel : [pixel of left up, pixel of right down]
    """
    up_left = p1
    down_right = p2
    target_local_position = marker_location_from_body(up_left, down_right, 0.185)
    target_xy_distance = np.sqrt(target_local_position[0]**2 + target_local_position[1]**2)
    print('xy_dis : ', target_xy_distance)
    center = (cx,cy)
    # Target_yaw = np.arctan2(target_local_position[1], target_local_position[0])*180/np.pi
    # Target_yaw=Target_yaw.item(0)
    lr, fb = 0, 0
    if centered_counter <40:
        print("target is:")
        print(target_xy_distance*100)
        if center[0] < (frameWidth/2) - deadZone:
            lr = -15
        elif center[0] > (frameWidth/2) + deadZone:
            lr = 15

        if center[1] < (frameHeight/2) - deadZone:
            fb = 15
        elif center[1] > (frameHeight/2) + deadZone:
            fb = -15

        if lr == 0 and fb == 0:
            tello.send_rc_control(0, 0, 0, 0)
            time.sleep(0.05)
            #print("send_rc_control(0, 8, 0, 0)")
            centered_counter += 1
        else:
            tello.send_rc_control(lr, 0, fb, 0)
            time.sleep(0.05)
            #print("send_rc_control({lr}, 0, {fb}, 0)")
            centered_counter = 0
            
        return False,centered_counter
    else:
        return True,centered_counter
        
        #drone.move_forward(int(target_xy_distance*100))


def Pid_second_phase(p1,p2, tello,cx,cy):
    """ Move drone to First Flag position
    color_marker_pixel : [pixel of left up, pixel of right down]
    """
    up_left = p1
    down_right = p2
    target_local_position = marker_location_from_body(up_left, down_right, 0.185)
    target_xy_distance = np.sqrt(target_local_position[0]**2 + target_local_position[1]**2)
    print('xy_dis : ', target_xy_distance)
    center = (cx,cy)
    # Target_yaw = np.arctan2(target_local_position[1], target_local_position[0])*180/np.pi
    # Target_yaw=Target_yaw.item(0)
    lr, fb = 0, 0
    
    "Go to Color Marker"
    if (target_xy_distance == np.inf):
        print("Inf is not recommened")
        return False
    elif (int(target_xy_distance*100) < 230): #++++
        print("target is too close")
        print(target_xy_distance*100)
        tello.send_rc_control(0,0,0,0)
        time.sleep(0.1)
        #tello.move_down(30)
        tello.move_up(30)
        time.sleep(3)
        return True
    else:
        print("target is:")
        print(target_xy_distance*100)
        if center[0] < (frameWidth/2) - deadZone:
            lr = -15
        elif center[0] > (frameWidth/2) + deadZone:
            lr = 15

        if center[1] < (frameHeight/2) - deadZone:
            fb = 15
        elif center[1] > (frameHeight/2) + deadZone:
            fb = -15

        if lr == 0 and fb == 0:
            tello.send_rc_control(0, 20, 0, 0)
            time.sleep(0.05)
            #print("send_rc_control(0, 8, 0, 0)")
            #centered_counter += 1
        else:
            tello.send_rc_control(lr, 0, fb, 0)
            time.sleep(0.05)
            #print("send_rc_control({lr}, 0, {fb}, 0)")
            #centered_counter = 0
            
        return False
        
        #drone.move_forward(int(target_xy_distance*100))


def Pid_second_phase2(p1,p2, tello,cx,cy):
    """ Move drone to First Flag position
    color_marker_pixel : [pixel of left up, pixel of right down]
    """
    up_left = p1
    down_right = p2
    target_local_position = marker_location_from_body(up_left, down_right, 0.185)
    target_xy_distance = np.sqrt(target_local_position[0]**2 + target_local_position[1]**2)
    print('xy_dis : ', target_xy_distance)
    center = (cx,cy)
    # Target_yaw = np.arctan2(target_local_position[1], target_local_position[0])*180/np.pi
    # Target_yaw=Target_yaw.item(0)
    lr, fb = 0, 0
    
    "Go to Color Marker"
    if np.isfinite(target_xy_distance) and int(target_xy_distance*100) < 130: #++++
        if (lr == 0 and fb == 0):
            print("target is too close")
            print(target_xy_distance*100)
            tello.send_rc_control(0,0,0,0)
            time.sleep(0.1)
            tello.move_down(30)
            #tello.move_up(30)
            time.sleep(1)
            return True
        else:
            if center[0] < (frameWidth/2) - deadZone2:
                lr = -6
            elif center[0] > (frameWidth/2) + deadZone2:
                lr = 6

            if center[1] < (frameHeight/2) - deadZone2:
                fb = 6
            elif center[1] > (frameHeight/2) + deadZone2:
                fb = -6
            tello.send_rc_control(lr, 0, fb, 0)
            time.sleep(0.05)
            return False
            
    else:
        print("target is:")
        print(target_xy_distance*100)
        if center[0] < (frameWidth/2) - deadZone:
            lr = -12
        elif center[0] > (frameWidth/2) + deadZone:
            lr = 12

        if center[1] < (frameHeight/2) - deadZone:
            fb = 12
        elif center[1] > (frameHeight/2) + deadZone:
            fb = -12

        if lr == 0 and fb == 0:
            tello.send_rc_control(0, 15, 0, 0)
            time.sleep(0.05)
            #print("send_rc_control(0, 8, 0, 0)")
            #centered_counter += 1
        else:
            tello.send_rc_control(lr, 0, fb, 0)
            time.sleep(0.05)
            #print("send_rc_control({lr}, 0, {fb}, 0)")
            #centered_counter = 0
            
        return False
        


def detect_and_draw_boxes(frame, model,desired):
    # centers = []
    is_number = False
    # print("start") 
    frame_tensor = torch.from_numpy(frame).float().permute(2, 0, 1).div(255.0).unsqueeze(0).cuda()
    #print("Shape of frame_tensor:", frame_tensor.shape)

    with torch.no_grad():
        pred = model(frame_tensor)[0]

    pred = non_max_suppression(pred, 0.4, 0.5)
    p1=0
    p2=0
    center_x=0
    center_y=0

    for i, det in enumerate(pred):
        # print("loop")
        if (det is not None and len(det)):
            det = det.cpu()
            # print("detect?")
            for *xyxy, conf, cls in reversed(det):
                #if (xyxy[0] <= 50) or (xyxy[0] >= 600) or (xyxy[1] <= 50) or (xyxy[1] >= 600): #++++
                    # print("Danger") #++++
                #    return p1,p2, center_x,center_y,is_number,frame #++++
                if (int((model.names[int(cls)])) == desired):
                    # print(model.names[int(cls)])
                    xyxy = np.array(xyxy).astype(int)
                    center_x = int((xyxy[0] + xyxy[2]) / 2)
                    center_y = int((xyxy[1] + xyxy[3]) / 2)
                    p1 = (xyxy[0],xyxy[1])
                    p2 = (xyxy[2],xyxy[3])
                    is_number = True
                    # centers.append((center_x, center_y))

                    cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 0), -1)
                    cv2.putText(frame, f"({center_x}, {center_y})", (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                    label = f"{model.names[int(cls)]} {conf:.2f}"
                    cv2.putText(frame, label, (xyxy[0], xyxy[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return p1,p2, center_x,center_y,is_number,frame

def detect_and_draw_boxes_init(frame, model):
    numbers = []
    is_number = False
    # print("start") 
    frame_tensor = torch.from_numpy(frame).float().permute(2, 0, 1).div(255.0).unsqueeze(0).cuda()
    #print("Shape of frame_tensor:", frame_tensor.shape)

    with torch.no_grad():
        pred = model(frame_tensor)[0]

    pred = non_max_suppression(pred, 0.4, 0.5)
    p1=0
    p2=0
    center_x=0
    center_y=0

    for i, det in enumerate(pred):
        #if (xyxy[0] <= 50) or (xyxy[0] >= 600) or (xyxy[1] <= 50) or (xyxy[1] >= 600): #++++
            # print("Danger") #++++
        #    return p1,p2, center_x,center_y,is_number,frame #++++
        # print("loop")
        if (det is not None and len(det)):
            det = det.cpu()
            # print("detect?")
            for *xyxy, conf, cls in reversed(det):
                # print("seeing number")
                # if (int((model.names[int(cls)])) == desired):
                    # print(model.names[int(cls)])
                xyxy = np.array(xyxy).astype(int)
                center_x = int((xyxy[0] + xyxy[2]) / 2)
                center_y = int((xyxy[1] + xyxy[3]) / 2)
                p1 = (xyxy[0],xyxy[1])
                p2 = (xyxy[2],xyxy[3])
                    # centers.append((center_x, center_y))
                number = int(model.names[int(cls)])
                numbers.append(number)
                is_number = True

                cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 0), -1)
                cv2.putText(frame, f"({center_x}, {center_y})", (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                label = f"{model.names[int(cls)]} {conf:.2f}"
                cv2.putText(frame, label, (xyxy[0], xyxy[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    return p1,p2, center_x,center_y,numbers,is_number,frame