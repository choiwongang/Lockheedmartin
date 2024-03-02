from djitellopy import Tello
import cv2
from time import sleep
from initialize2 import *


def searching_rectangle(red_rectangle, 
                        green_rectangle,
                        blue_rectangle,
                        num,
                        is_red_rectangle,
                        is_green_rectangle,
                        is_blue_rectangle,
                        is_num,
                        tello,
                        r_n,
                        l_n,
                        n,
                        i,
                        red_counter,
                        green_counter,
                        blue_counter,
                        num_counter) :
    print("search")
    M = 80
    print("r_n:",r_n, "l_n",l_n,"n:",n,"i:",i,"red_counter:",red_counter,"blue_counter :","num_counter :",num_counter)
    if(red_rectangle == True):
        if (r_n == 0) and (l_n == 0) and (n % 8 == 0) and (i<50):
            i+=1
            #print(f"First right move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            if is_red_rectangle:
                ##print("is_red_rectangle")
                red_counter += 1
            else:
                #print("red_counter")
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                ##print("tello move right M")
                tello.move_right(M)
                #print("???????????????????????????????????????????")
                sleep(2)
                r_n += 1
                n += 1
                i = 0
        elif (r_n ==1) and (n% 8 ==1) and(i<50):
            #print("/////////////////////////")
            i+=1
            #print(f"Right move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n == 2) and (n % 8 == 2) and (i<50):
            #print(f"Switch to left after 4 right moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i += 1
            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                r_n -= 1
                n += 1
                i=0
        elif (r_n ==1) and (n % 8 ==3) and (i<50):
            #print(f"Continue left until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i +=1
            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0
                    
        elif (r_n == 0) and (l_n == 0) and (n % 8 == 4) and (i<50):
            #print(f"First left move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n ==1) and (n % 8 ==5)and (i<50):
            #print(f"Left move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i +=1

            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15:
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n == 2) and (n % 8 == 6)and(i<50):
            #print(f"Switch to right after 4 left moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
        elif (l_n ==1) and (n % 8 ==7)and(i<50):
            #print(f"Continue right until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_red_rectangle:
                red_counter += 1
            else:
                red_counter = 0
            if red_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
    elif(green_rectangle == True):
        if (r_n == 0) and (l_n == 0) and (n % 8 == 0)and(i<50):
            #print(f"First right move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n ==1) and (n%8==1) and(i<50):
            #print(f"Right move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n == 2) and (n % 8 == 2) and (i<50):
            #print(f"Switch to left after 4 right moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0
        elif (r_n ==1) and (n % 8 ==3) and(i<50):
            #print(f"Continue left until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0

        elif (r_n == 0) and (l_n == 0) and (n % 8 == 4) and (i<50):
            #print(f"First left move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n ==1) and (n % 8 ==5) and(i<50):
            #print(f"Left move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n == 2) and (n % 8 == 6)and(i<50):
            #print(f"Switch to right after 4 left moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0

        elif (l_n ==1) and (n % 8 == 7)and(i<50):
            #print(f"Continue right until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_green_rectangle:
                green_counter += 1
            else:
                green_counter = 0
            if green_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
    elif(blue_rectangle == True):
        if (r_n == 0) and (l_n == 0) and (n % 8 == 0)and(i<50):
            #print(f"First right move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n ==1) and(n%8 ==1) and(i<50):
            #print(f"Right move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n == 2) and (n % 8 == 2) and (i<50):
            #print(f"Switch to left after 4 right moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0
        elif (r_n ==1) and (n % 8 ==3) and (i<50):
            #print(f"Continue left until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0

        elif (r_n == 0) and (l_n == 0) and (n % 8 == 4)and(i<50):
            #print(f"First left move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n ==1) and (n % 8 ==5) and (i<50):
            #print(f"Left move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n == 2) and (n % 8 == 6) and (i<50):
            #print(f"Switch to right after 4 left moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
        elif (l_n ==1) and (n % 8 ==7) and(i<50):
            #print(f"Continue right until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_blue_rectangle:
                blue_counter += 1
            else:
                blue_counter = 0
            if blue_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
    elif(num == True):
        if (r_n == 0) and (l_n == 0) and (n % 8 == 0)and(i<50):
            print(f"First right move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                print("case1")
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n ==1) and (n%8 ==1) and (i<50):
            #print(f"Right move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                r_n += 1
                n += 1
                i=0
        elif (r_n == 2) and (n % 8 == 2)and(i<50):
            #print(f"Switch to left after 4 right moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0
        elif (r_n == 1) and (n % 8 ==3)and(i<50):
            #print(f"Continue left until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
        
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                r_n -= 1
                n += 1
                i=0

        elif (r_n == 0) and (l_n == 0) and (n % 8 == 4)and(i<50):
            #print(f"First left move (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
    
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n == 1) and (n % 8 ==5) and(i<50):
            #print(f"Left move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i +=1
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_left(M)
                sleep(2)
                l_n += 1
                n += 1
                i=0
        elif (l_n == 2) and (n % 8 == 6)and(i<50):
            #print(f"Switch to right after 4 left moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):  
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
        elif (l_n == 1) and (n % 8 == 7)and(i<50):
            #print(f"Continue right until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
            i+=1
            if is_num:
                num_counter += 1
            else:
                num_counter = 0
            if num_counter >= 15: 
                return r_n,l_n,True,n,i,red_counter,green_counter,blue_counter,num_counter
            if(i==49):
                tello.move_right(M)
                sleep(2)
                l_n -= 1
                n += 1
                i=0
    
    return r_n,l_n,False,n,i,red_counter,green_counter,blue_counter,num_counter