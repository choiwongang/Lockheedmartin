from djitellopy import Tello
import cv2
from time import sleep
from initialize2 import *

###########################init####################
def searching_rectangle_init(
                        is_num,
                        tello,
                        r_n,
                        l_n,
                        n,
                        i,
                        num_counter,
                        numbers,
                        used_numbers) : 
    M = 80
    if (r_n == 0) and (l_n == 0) and (n % 8 == 0) and (i<50):
        i+=1
        #print(f"First right move (r_n: {r_n}, l_n: {l_n}, n: {n})")
        if is_num:
            num_counter += 1
            #print(num_counter)
        else:
            num_counter = 0
            #print(num_counter)
        if num_counter >= 15:
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                print(used_numbers)
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            #print("이거 맞음?")
            tello.move_right(M)
            #print("???????????????????????????????????????????")
            sleep(2)
            r_n += 1
            n += 1
            i = 0
    elif (r_n == 1) and(n%8 == 1)and(i<50):
        #print("/////////////////////////")
        i+=1
        #print(f"Right move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
        if is_num:
            num_counter += 1
        else:
            num_counter = 0
        if num_counter >= 15: 
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            ##print("1")
            tello.move_right(M)
            sleep(2)
            r_n += 1
            n += 1
            i = 0
    elif (r_n == 2) and (n % 8 == 2) and (i<50):
        #print(f"Switch to left after 4 right moves (r_n: {r_n}, l_n: {l_n}, n: {n})")
        i += 1
        if is_num:
            num_counter += 1
        else:
            num_counter = 0
        if num_counter >= 15: 
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            tello.move_left(M+20)
            sleep(2)
            r_n -= 1
            n += 1
            i=0
    elif (r_n ==1) and (n%8==3)and (i<50):
        #print(f"Continue left until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
        i +=1
        if is_num:
            num_counter += 1
        else:
            num_counter = 0
        if num_counter >= 15: 
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            tello.move_left(M+20)
            sleep(2)
            r_n -= 1
            n += 1
            i=0  
    elif (r_n == 0) and (l_n == 0) and (n % 8 == 4) and (i<50):
        #print(f"First left move (r_n: {r_n}, l_n: {l_n}, n: {n})")
        i+=1
        if is_num:
            num_counter += 1
        else:
            num_counter = 0
        if num_counter >= 15: 
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            tello.move_left(M+20)
            sleep(2)
            l_n += 1
            n += 1
            i=0
    elif (l_n == 1) and (n%8 == 5) and (i<50):
        #print(f"Left move until 1/4 (r_n: {r_n}, l_n: {l_n}, n: {n})")
        i +=1

        if is_num:
            num_counter += 1
        else:
            num_counter = 0
        if num_counter >= 15: 
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            tello.move_left(M+20)
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
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            tello.move_right(M)
            sleep(2)
            l_n -= 1
            n += 1
            i=0
    elif (l_n == 1) and (n % 8 ==7)and(i<50):
        #print(f"Continue right until starting point (r_n: {r_n}, l_n: {l_n}, n: {n})")
        i+=1
        if is_num:
            num_counter += 1
        else:
            num_counter = 0
        if num_counter >= 15: 
            used_numbers = match_numbers(numbers,used_numbers)
            if len(used_numbers) == 3:
                return r_n,l_n,True,n,i,num_counter,used_numbers
        if(i==49):
            tello.move_right(M)
            sleep(2)
            l_n -= 1
            n += 1
            i=0
    return r_n,l_n,False,n,i,num_counter,used_numbers
    