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

def QRCodeMulti(det, image):
    is_qr = False
    infos, box_coordinates, _ = det.detectAndDecodeMulti(image)
    if len(infos) >= 1:
        for info, box in zip(infos, box_coordinates):
            print(info)
            box = box.astype(int)
            n = len(box)
            for i in range(n):
                cv2.line(image, tuple(box[i]), tuple(box[(i+1) % n]), (0,255,0), 3)
            
            # Calculate position for text (roughly bottom-left corner of QR code)
            text_position = tuple(box[3])
            
            # Add text to image
            cv2.putText(image, info, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            is_qr = True
    return image, infos, is_qr

def CannyColor(binary_image):
    # Apply a Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(binary_image, (5, 5), 0)
    # Use adaptive thresholding
    adaptive = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Apply Canny edge detection
    canny_image = cv2.Canny(adaptive, 30, 150)
    # Dilate the edges to make them more pronounced
    dilated = cv2.dilate(canny_image, None, iterations=2)
    return dilated

def ColorThreshold(image):
    # Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Threshold based on the input range
    red_range_low = np.array([0, 50, 50])
    red_range_high = np.array([10, 255, 255])
    red_mask = cv2.inRange(hsv, red_range_low, red_range_high)
    red_canny = CannyColor(red_mask)

    green_range_low = np.array([40, 40, 40])
    green_range_high = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, green_range_low, green_range_high)
    green_mask = cv2.GaussianBlur(green_mask,(9,9),0)
    green_canny = CannyColor(green_mask)

    # blue_range_low = np.array([90, 60, 60])
    blue_range_low = np.array([90, 60, 60])
    blue_range_high = np.array([150, 255, 255])
    blue_mask = cv2.inRange(hsv, blue_range_low, blue_range_high)
    blue_mask = cv2.GaussianBlur(blue_mask,(9,9),0)
    blue_canny = CannyColor(blue_mask)
    
    return red_canny, green_canny, blue_canny, image

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

def FindRectangle(canny_image,original_image):
    is_tri = False
    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt) # This is used to find the area of the contour.
        print("Area: ",area)
        if (area > 1000): # The areas below 500 pixels will not be considered
            perimeter = cv2.arcLength(cnt, True) # The true indicates that the contour is closed
            # print("Perimeter: ", perimeter)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True) # This method is used to find the approximate number of contours
            # print("Corner Points: ", len(approx))
            objCorner = len(approx)
            x,y,w,h = cv2.boundingRect(approx) # In this we get the values of our bounding box that we will draw around the object

            if objCorner == 4:
                shape_name = "Rectangle"
                cv2.drawContours(original_image, cnt, -1, (255,255,255), 3) # -1 denotes that we need to draw all the contours
                is_tri = True
    return canny_image,original_image, is_tri

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