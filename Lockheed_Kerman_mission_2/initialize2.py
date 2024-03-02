
def match_numbers(numbers,number_counter):
    # 사용된 숫자를 추적하기 위한 집합을 초기화합니다.
    used_numbers = []

    # 각 사각형 링의 정보를 하나씩 처리합니다.
    for i in range(len(numbers)):
        print("this is length",len(numbers))
        # print(i)
        # 입력으로 받은 숫자와 해당 숫자의 좌표를 사용합니다.
        number = numbers[i]
        print("what",number)
        if not(number in used_numbers):
            print("the",number)            
            used_numbers.append(number)
        else :
            print("same number detect")
            
            
    print("fuck")
    # 색상과 숫자를 매칭한 결과를 반환합니다.
    return used_numbers