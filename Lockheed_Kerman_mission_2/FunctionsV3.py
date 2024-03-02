import cv2
import numpy as np

def QRCode(det, image):
    is_qr = False
    info = None
    info, box_coordinates, _ = det.detectAndDecode(image)
    if (len(info) >= 1) and (box_coordinates is not None):
        print(info)
        box_coordinates = box_coordinates[0].astype(int)
        n = len(box_coordinates)
        for i in range(n):
            cv2.line(image, tuple(box_coordinates[i]), tuple(box_coordinates[(i+1) % n]), (0,255,0), 3)
        
        # Calculate position for text (roughly bottom-left corner of QR code)
        text_position = tuple(box_coordinates[3])

        # Add text to image
        cv2.putText(image, info, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        
        is_qr = True
    return image, info, is_qr

def CannyColor(gray_image):
    # Apply a Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Use adaptive thresholding
    adaptive = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Apply Canny edge detection
    canny_image = cv2.Canny(adaptive, 30, 300) # 30 300
    # canny_image = cv2.Canny(gray_image,30,150)
    # Dilate the edges to make them more pronounced
    dilated = cv2.dilate(canny_image, None, iterations=2)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt) # This is used to find the area of the contour.
        #print("Area: ",area)
        if (area > 0): # The areas below 500 pixels will not be considered
            perimeter = cv2.arcLength(cnt, True) # The true indicates that the contour is closed
            # print("Perimeter: ", perimeter)
            approx = cv2.approxPolyDP(cnt, 0.08*perimeter, True) # This method is used to find the approximate number of contours
            # print("Corner Points: ", len(approx))
            objCorner = len(approx)
            # x,y,w,h = cv2.boundingRect(approx) # In this we get the values of our bounding box that we will draw around the object

            if objCorner == 4: # This condition considers anything with 3 corners as a triangle
                cv2.drawContours(dilated, cnt, -1, (255, 255, 255), 3) # Draw the triangle
    
    return canny_image

def ColorThreshold(frame):
    # frame is RGB image

    # color parameters for color abstraction
    red_range_low = np.array([118, 19, 62])
    red_range_high = np.array([132, 255, 120])
    green_range_low = np.array([0, 116, 0])
    green_range_high = np.array([47, 213, 80])
    blue_range_low = np.array([0, 108, 80])
    blue_range_high = np.array([16, 255, 146])

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    red_mask = cv2.inRange(hsv, red_range_low, red_range_high)
    green_mask = cv2.inRange(hsv, green_range_low, green_range_high)
    blue_mask = cv2.inRange(hsv, blue_range_low, blue_range_high)

    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    green_contours,_ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    blue_contours,_ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in red_contours:
        area = cv2.contourArea(cnt)
        if (area > 10000):
            perimeter = cv2.arcLength(cnt, True)
            
            approx = cv2.approxPolyDP(cnt, 0.08*perimeter, True)
            
            objCorner = len(approx)
            
            if objCorner == 4:
                cv2.drawContours(red_mask, cnt, -1, (255, 255, 255), 3)
    
    for cnt in green_contours:
        area = cv2.contourArea(cnt)
        if (area > 10000):
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.08*perimeter, True)
            objCorner = len(approx)

            if objCorner == 4:
                cv2.drawContours(green_mask, cnt, -1, (255, 255, 255), 3)
    
    for cnt in blue_contours:
        area = cv2.contourArea(cnt)
        if (area > 10000):
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.08*perimeter, True)
            objCorner = len(approx)

            if objCorner == 4:
                cv2.drawContours(blue_mask, cnt, -1, (255, 255, 255), 3)

    return red_mask,green_mask,blue_mask, frame

def FindCircle(canny_image,original_image):
    is_circle = False
    center = None
    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt) # This is used to find the area of the contour.
        # print("Area: ",area)
        if (area > 12000): # The areas below 500 pixels will not be considered
            perimeter = cv2.arcLength(cnt, True) # The true indicates that the contour is closed
            # print("Perimeter: ", perimeter)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True) # This method is used to find the approximate number of contours
            # print("Corner Points: ", len(approx))
            objCorner = len(approx)
            x,y,w,h = cv2.boundingRect(approx) # In this we get the values of our bounding box that we will draw around the object

            if objCorner > 6:
                shape_name = "circle"
                print(shape_name)
                # cv2.drawContours(original_image, cnt, -1, (255,255,255), 3) # -1 denotes that we need to draw all the contours
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                cv2.circle(original_image, center, int(radius), (255, 255, 255), 3) # Draw the circle
                cv2.circle(original_image, center, 5, (255, 255, 255), -1) # Draw the center of the circle
                text = f"Center: ({int(x)}, {int(y)})"
                cv2.putText(original_image, text, (int(x) - 60, int(y) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2) # Put the text

                is_circle = True
    return canny_image,original_image, is_circle, center

def FindRectangle(canny_image,original_image,color):
    is_rectangle = False
    center = None
    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt) # This is used to find the area of the contour.
        #print("Area: ",area)
        if (area > 10000): # The areas below 500 pixels will not be considered
            perimeter = cv2.arcLength(cnt, True) # The true indicates that the contour is closed
            # print("Perimeter: ", perimeter)
            approx = cv2.approxPolyDP(cnt, 0.08*perimeter, True) # This method is used to find the approximate number of contours
            # print("Corner Points: ", len(approx))
            objCorner = len(approx)
            x,y,w,h = cv2.boundingRect(approx) # In this we get the values of our bounding box that we will draw around the object

            if objCorner == 4: # This condition considers anything with 3 corners as a triangle
                # shape_name = "rectangle"
                M = cv2.moments(cnt) # Calculate moments of the contour
                x = int(M["m10"] / M["m00"]) # Calculate x coordinate of center
                y = int(M["m01"] / M["m00"]) # Calculate y coordinate of center
                center = (x, y)
                cv2.drawContours(original_image, cnt, -1, (255, 255, 255), 3) # Draw the triangle
                cv2.circle(original_image, center, 5, (0, 0, 255), -1) # Draw the center of the triangle
                
                if color == 0: # red
                    text = f"Red Center: ({x}, {y})"
                elif color == 1: # green
                    text = f"Green Center: ({x}, {y})"
                else:           # blue
                    text = f"Blue Center: ({x}, {y})"
                cv2.putText(original_image, text, (x - 60, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Put the text
                is_rectangle = True
    return canny_image, original_image, is_rectangle, center

def FindTriangle(canny_image,original_image):
    is_tri = False
    center = None
    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt) # This is used to find the area of the contour.
        # print("Area: ",area)
        if (area > 10000): # The areas below 500 pixels will not be considered
            perimeter = cv2.arcLength(cnt, True) # The true indicates that the contour is closed
            # print("Perimeter: ", perimeter)
            approx = cv2.approxPolyDP(cnt, 0.08*perimeter, True) # This method is used to find the approximate number of contours
            # print("Corner Points: ", len(approx))
            objCorner = len(approx)
            x,y,w,h = cv2.boundingRect(approx) # In this we get the values of our bounding box that we will draw around the object

            if objCorner == 3: # This condition considers anything with 3 corners as a triangle
                shape_name = "triangle"
                M = cv2.moments(cnt) # Calculate moments of the contour
                x = int(M["m10"] / M["m00"]) # Calculate x coordinate of center
                y = int(M["m01"] / M["m00"]) # Calculate y coordinate of center
                center = (x, y)
                cv2.drawContours(original_image, cnt, -1, (255, 255, 255), 3) # Draw the triangle
                cv2.circle(original_image, center, 5, (0, 0, 255), -1) # Draw the center of the triangle
                text = f"Center: ({x}, {y})"
                cv2.putText(original_image, text, (x - 60, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Put the text
                is_tri = True

    return canny_image, original_image, is_tri, center