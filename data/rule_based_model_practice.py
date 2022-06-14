import os
import pandas as pd
import pickle
import re
from multiprocessing.connection import answer_challenge
cp=os.getcwd()
print(cp)
print(os.listdir(cp))
# 특수문자 제거하기
def remove_else(input):
    new_string = ''.join(filter(str.isalnum, input))
    return new_string
# 언어 확인
def isEnglishOrKorean(input):
    k_count = 0
    e_count = 0
    length=len(input)
    for c in input:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    if k_count==length:
        return "한국어"  
    elif e_count==length:
        return "영어" 
    elif k_count+e_count>=length-1:
        return 'mixed'
    else:
        return 'else'
# 이름인지 확인
def isname(input,input_original,language,last_name_list,last_name_list_en,first_name_list):
    # 변수 선언
    cnt=0
    a=0
    answer=0
    #특수문자로 이름 판별
    for i in input_original:
        if ((ord('0') <= ord(i) <= ord('9')) 
         or (ord('가') <= ord(i) <= ord('힣'))
         or (ord('a') <= ord(i.lower()) <= ord('z'))
         or ord('A') <= ord(i.lower()) <= ord('Z')
         or i=='-'
         or i==' '
         or i==')'
         or i=='('
        ):
            continue
        else:
            cnt+=1
    if cnt>=1:
        return answer,0
    if language=="한국어":
        if input[0] in last_name_list:
            if input[1:] in first_name_list:
                answer="1Name: "+input
    #영어 성씨 추가 필요
    elif language=="영어":
        for last_name_en in last_name_list_en:
            # if last_name_en=="kim":
            # if len(input)>len(last_name_en):
            #     print(input[0:len(last_name_en)] == last_name_list_en)
            #     print(input,len(input),input[0:len(last_name_en)],len(last_name_en),"kim")
            if (input[0:len(last_name_en)] == last_name_en) and len(input)<25:
                answer="2English name: "+ input
    #혼합되어 있는 경우
    elif language=="mixed":
        if (ord('가') <= ord(input[0]) <= ord('힣')):
            ch='k'
        else:
            ch='e'
        for i in range(len(input)):
            if (ord('가') <= ord(input[i]) <= ord('힣')):
                ch2='k'
            else:
                ch2='e'
            if ch!=ch2:
                a=i
                if ch=='k':
                    if input[0] in last_name_list:
                        if input[1:i] in first_name_list:
                            answer= "1Name: "+input[0:i]
                else:
                    for last_name_en in last_name_list_en:
                        if (input[0:len(last_name_en)] == last_name_en):
                            answer="2English name: "+ input[0:i]
                break
    return answer,a


# 전화번호인지 확인
def isnum(input,input_original,catbef):
    a=0
    fax=["fax"]
    tel=["tel","t"]
    phone=["phone","mobile","m"]
    temp=''
    # 앞자리 리스트 만들기
    nat_list=['82']
    phone_list=['010','011','017']
    n_phone_list=[]
    for phone in phone_list:
        temp=phone[1:]
        n_phone_list.append(temp)
    tel_list=['02','051','053','032', '062','042','052','044','031','033','043','041','063','061','054','055','064','070']
    n_tel_list=[]
    for tel in tel_list:
        temp=tel[1:]
        n_tel_list.append(temp)

    # 종류 구분하기
    cat=''
    small_input=input_original.lower()
    temp=''
    for c in input:
        if ord('0') <= ord(c) <= ord('9'):
            temp+=c
    for nat_num in nat_list:
        if len(nat_num)<len(temp):
            if nat_num==temp[0:len(nat_num)]:
                if temp[len(nat_num):len(nat_num)+2] in n_phone_list:
                    cat="phone"
                elif temp[len(nat_num):len(nat_num)+2] in n_tel_list or  temp[len(nat_num):len(nat_num)+1]=='02':
                    for fax_str in fax:
                        if fax_str in input:
                            cat="fax" 
                    else:
                        cat="tel"
    if cat=="":
        if temp[0:3] in phone_list:
            cat="phone"
        elif temp[0:3] in tel_list or temp[0:2]=='02':
            for fax_str in fax:
                # if fax_str in small_input:
                if fax_str in input[0:9]:
                    cat="fax"
                # print(temp,small_input)               
            if cat=='':
                cat="tel"
        else:
            return 0, 0

    # for fax_str in fax:
    #     if fax_str in small_input:
    #         cat="fax"
    # for tel_str in tel:
    #     if tel_str in  small_input:
    #         cat="tel"
    # for phone_str in phone:
    #     if phone_str in  small_input:
    #         cat="phone"
    # else:
    #     if temp[0:2] in nat_list:
    #         if temp[2:4] in n_phone_list or temp[0:3] in phone_list:
    #             cat="phone"
    #         elif temp[2:4] in n_tel_list or  temp[0:3] in n_tel_list:
    #             if catbef=="tel" or catbef=="fax":
    #                 cat="fax"
    #             else:
    #                 cat="tel"
    #         else:
    #             return 0
    
    
    
    # 번호면 print, 숫자 아닌 것 연속으로 3개 나오면 끊기
    temp=''
    for c in range(len(input)):
        if ord('0') <= ord(input[c]) <= ord('9'):
            temp+=input[c]
            cnt=0
        elif temp!='' and (ord('0') >= ord(input[c]) or ord(input[c]) >= ord('9')):
            cnt=cnt+1
            if cnt>1:
                a=c-cnt+1
                break
                # isnum(input[c-2:],input_original[c-2:],1)

    # for c in range(len(input_original)):
    #     if ord('0') <= ord(input_original[c]) <= ord('9'):
    #         new_num=input_original[c:]
    #         for d in range(len(new_num)):
    #             if ord('0') <= ord(input_original[d]) <= ord('9'):
    #                 temp+=input_original[d]
    #             else:
    #                 break
    #         break
    if temp.isdigit()==True and len(temp)<=13 and len(temp)>=9:
        number="3"+cat+": "+temp
        print(number)
        return number, a
    else:
        return 0, 0

# 직위/직책인지 확인
def isposition(input_original, position_list):
    # 직위 직책 리스트 추가 필요, 조건을 뒤에 포함 느낌으로 바꿔야 함
    for position in position_list:
        if position in input_original:
            pos_answer="4Position: " +input_original
            return pos_answer
    else:
        return 0
# 이메일인지 확인
def isemail(input_original):
    if '@' in input_original:
        pos_answer="5E-mail: " +input_original
        return pos_answer
    else:
        return 0

# 파일 불러오기
with open("./pickle/last_name_list.pickle","rb") as f:
    last_name_list = pickle.load(f)
with open("./pickle/first_name_list.pickle","rb") as f:
    first_name_list = pickle.load(f)
with open("./pickle/last_name_list_en.pickle","rb") as f:
    last_name_list_en_temp = pickle.load(f)
with open("./pickle/position_list.pickle","rb") as f:
    position_list = pickle.load(f)
last_name_list_en=[]
for i in last_name_list_en_temp:
    a=i.lower()
    last_name_list_en.append(a)

#main
def mainfun(inputlist):
    #input change
    answer=[]
    input_changed=[]
    catbef=""
    for i in range(len(inputlist)):
        temp=remove_else(inputlist[i])
        temp=temp.lower()
        input_changed.append(temp)
    # print(input_changed)
    for i in range(len(input_changed)):
        # print(input_changed[i])
        f=0
        alpha=0 
        chalpha=0
        chbeta=0
        if input_changed!='':
            language=isEnglishOrKorean(input_changed[i])
            c = isposition(inputlist[i],position_list)
            if c==0:
                while alpha>0 or chalpha==0:
                    chalpha=1
                    ans,alpha = isname(input_changed[i][alpha:],inputlist[i][alpha:],language,last_name_list,last_name_list_en,first_name_list)
                    language=isEnglishOrKorean(input_changed[i][alpha:])
                    if a!=0:
                        answer.append(ans)
            while f>0 or chbeta==0:
                chbeta=1
                b, f = isnum(input_changed[i][f:],inputlist[i][f:],catbef)
                if b!=0:
                    answer.append(b)
            d = isemail(inputlist[i])
        if c!=0:
            answer.append(c)
        if d!=0:
            answer.append(d)
    n_answer=[]
    for i in answer:
        if type(i)==type("str"):
            n_answer.append(i)
    n_answer.sort()
    for i in n_answer:
        print(i[1:])
    print('----------------------')

# inputlist=['Tel','Adress서울시구로디지털로123미리빌딩1층303호먼지상점',
# 'Mobile01032420900',
# '김먼지','|nsta',
# 'Kakaostore_dust',
# '대표',
# '4store1dust']
# inputlist2=['(주)지금융코리아',
#  '?<1',
#  'Good|.N9I1질※onaCoLL/1',
#  '서울영등포구선유로13길25.513호',
#  'TEL:070-1324-1234/FAX:070-1234-1234',
#  'Mobile:010-1234-5678',
#  'E-øa1:GIK2020ønaver.com',
#  '차은우',
#  '00지점I팀장']
# inputlist3=['KIMTAEHEE',
#  'GENERALMANAGER',
#  '13,TAEBOKSAN-RO3BEON-GIL,UICHANG-GU,CHANGWON-SI,',
#  'GYEONGSANGNAM-DO.RepublicOFKOREA',
#  '055.282.0321',
#  'CLOSEPM12:00',
#  'OPENPM06:00']
# inputlist4=['재무관리실회계팀',
#  '과장',
#  'T07012345678',
#  'M01012345678',
#  'Ekim00@taekWang.cokr',
#  '태광산업주식회사',
#  '04616서울시중구동호로310',
#  '김태광',
#  '태광산업']
# inputlist5=['김지현(kimjiwonom)',
# 'kimjiwonon(김자현)',
# 'jiwon-kim',
# 'kim ji-won',
# '전민규',
# '김민규',
# '전지원',
# '정 준우',
# 'KimJiwon',
#  '구  창  회',
#  '과장',
#  'A팀부장',
#  'ceo',
#  'CEO',
#  'T07012345678',
#  'T070-1234-5678',
#  'fax07012341342',
#  '(+)82-10-5364-5693',
#  '8210-5364-5693',
#  '827012345678',
#  'Ekim00@taekWang.cokr',
#  '04616서울시중구동호로310',
#  '태광산업']
inputlist6=['T.043-5502-3185F.02-124-1374M.010-7378-9487']
# mainfun(inputlist)
# mainfun(inputlist2)
# mainfun(inputlist3)
# mainfun(inputlist4)
# mainfun(inputlist5)
mainfun(inputlist6)