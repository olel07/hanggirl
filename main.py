import re
import matplotlib.pyplot as plt
import cv2
from matplotlib.image import imread
from random import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
#import libraries
#1. matplotlib
#2. opencv-python
#3. beautifulSoup

class BaseInfo:
    def __init__(self):
        self.subnum = ""
        self.subject = ""
        self.intro = "을(를) 선택하셨습니다. 힌트를 보고 알파벳을 맞추세요."
        self.line = "===================================================================="

    def setsubnum(self, subnum):
        self.subnum = subnum

    def setsubject(self, subject):
        self.subject = subject

    def gameintro(self):
        print(self.line)
        print("=              Hang Girl Game에 오신 것을 환영합니다!              =")
        print(self.line)
        print("여가 시간에 무엇을 할지 행걸게임을 통해 정하고자 합니다.")
        print("아래 주제 중 하나를 정하고 번호를 입력하세요(ex : 1)")
        print(self.line)
        print("                    0. 게임 가이드")
        print("                    1. 식당 방문")
        print("                    2. 영화 보기")
        print("                    3. 잠이나 잘래요.(게임종료)")
        print(self.line)
        self.setsubnum(input("> 내가 정한 주제는 : "))
        print(self.line)


class StartGame:
    def __init__(self):
        self.title = ""
        self.tiList = []
        self.ansList = []
        self.answer = ""

    def converttotitle(self, originTitle):  # 정규표현식을 통해 타이틀 획득
        title = re.sub('[0-9-=+,#/|?:^$.@*\()"]', '', originTitle)  # 특수문자 및 숫자 제거
        title = re.sub('^[\s]', '', title)  # 맨 앞 공백 제거
        title = re.sub('[\s]$', '', title)  # 맨 뒤 공백 제거

        c = re.search("([a-zA-Z]*(\s|')*)*", title)  # 정규표현식에 맞게 title 가져오기
        if c == None:
            return None
        else:
            return str(c.group())

    def crawltofranchise(self):  # 1. 식당 방문
        html = urlopen("https://www.businessinsider.com/top-food-franchises-in-america-2016-1#15-baskin-robbins-2")
        bsobj = BeautifulSoup(html.read(), "html.parser")
        section = bsobj.find("div", {"class": "slide-title clearfix"})  # 타이틀을 포함하고 있는 h2 태그 찾아옴
        # print(section)

        for title in bsobj.find_all("h2", {"class": "slide-title-text"}):
            title = title.text.strip()
            title = self.converttotitle(title)
            # print(title)
            tilen = len(title)
            if 6 < tilen < 20:  # 기회는 6번이기 때문에 길이 6자 이상만 가져옴 and 너무 길면 어려우니 20자
                self.tiList.append(title)

        # 타이틀 리스트에서 랜덤하게 가져옴
        i = randint(0, len(self.tiList) - 1)
        self.answer = self.tiList[i]
        self.answer = self.answer.lower()
        self.ansList = list(self.answer)

    def crawltomovie(self):
        html = urlopen("https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/")
        bsobj = BeautifulSoup(html.read(), "html.parser")
        section = bsobj.find("div", {"id": "main_container"})  # 타이틀을 포함하고 있는 div 태그 찾아옴

        for title in section.find_all("a", {"class": "unstyled articleLink"}):  # 타이틀이 명시되어 있는 a 태그만 찾아옴
            title = title.text.strip()
            if (title != "View All"):  # 필요없는 태그 예외
                title = self.converttotitle(title)
                tilen = len(title)
                if 6 < tilen < 20:  # 기회는 6번이기 때문에 길이 6자 이상만 가져옴 and 너무 길면 어려우니 20자
                    self.tiList.append(title)

        # 타이틀 리스트에서 랜덤하게 가져옴
        i = randint(0, len(self.tiList) - 1)
        self.answer = self.tiList[i]
        self.answer = self.answer.lower()
        self.ansList = list(self.answer)


class PlayGame:
    def __init__(self):
        self.title = ""
        self.ansList = []
        self.answer = ""
        self.cusList = []
        self.life = 6
        self.hangnum = 1
        self.hanggirl = ""

    def setansList(self, ansList):
        self.ansList = ansList

    def setanswer(self, answer):
        self.answer = answer

    def setcuslist(self, ansList):
        for ansalpha in ansList:
            ansalpha = re.sub('[a-zA-Z"]', '_', ansalpha)  # 정답맞추기용 힌트
            self.cusList.append(ansalpha)
        print("힌트 : ")
        print(self.cusList)

    def sethanggirl(self):#행걸 이미지 출력용
        self.hanggirl = 'hanggirl' + str(self.hangnum) + '.png'
        self.hangnum = self.hangnum + 1


    def updatecuslist(self, alpha):
        print("남은 LIFE ", "★"*(self.life-1))
        alpha = alpha.lower()
        x = 0
        idx = 0

        r = re.compile('[a-z]')
        match = r.search(alpha)
        if(match == None):
            print("영어만 입력하세요.")
            return False

        while x != -1: #정답 내 모든 알파벳 찾기 위함
            x = self.answer.find(alpha)  # 단어 위치
            if x != -1:
                self.answer = self.answer[0:x] + '_' + self.answer[x+1:] #중복검사 방지
                self.cusList[x] = alpha
                idx = idx + 1
        print(self.cusList)
        if idx == 0:
            self.life = self.life - 1 #알파벳이 포함되어 있지 않으면 life 깎기
            self.sethanggirl()
            img = cv2.imread(self.hanggirl,0)
            cv2.namedWindow(self.hanggirl, cv2.WINDOW_NORMAL)
            cv2.imshow(self.hanggirl,img)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()

an = BaseInfo()
st = StartGame()
pl = PlayGame()
sucess = False

an.gameintro()


if an.subnum == '0':
    print("두 개의 주제 중 하나를 골라서 타이틀을 맞추는 게임입니다.")
    print("힌트를 보고 몇 글자의 알파벳인지 확인하세요.")
    print("목숨은 총 6개이며 틀릴 때마다 그림이 출력됩니다.")
    print(an.line)
    quit()
elif an.subnum == '1':
    an.setsubject("식당 방문")
    print(an.subject + an.intro)#인사말
    print(an.line)
    st.crawltofranchise() #식당 타이틀
elif an.subnum == '2':
    an.setsubject("영화 보기")
    print(an.subject + an.intro)  # 인사말
    print(an.line)
    st.crawltomovie() #영화 타이틀
elif an.subnum == '3':
    print("좋은 꿈 꾸세요^~^")  # 인사말
    print(an.line)
    quit()

#게임진행
pl.setanswer(st.answer)#papa john's
pl.setansList(st.ansList)#['p', 'a', 'p', 'a', ' ', 'j', 'o', 'h', 'n', "'", 's']
pl.setcuslist(st.ansList)
while pl.ansList != pl.cusList and pl.life > 0:
    print(an.line)
    pl.updatecuslist(input("> 알파벳입력 : "))
    print(an.line)

if pl.life == 0:
    print("게임에서 졌습니다.")
else:
    print("게임에서 이겼습니다.")