import re
import cv2
from random import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
# import libraries
# 1. opencv-python
# 2. beautifulSoup

# 게임 소개 클래스
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

# 게임 시작 클래스
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

    # 1. 식당 방문 타이틀 세팅
    def crawltofranchise(self):  
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

    # 2. 영화 타이틀 세팅
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

# 게임 진행 클래스
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

    # 행걸 이미지 출력용
    def sethanggirl(self):
        self.hanggirl = 'hanggirl' + str(self.hangnum) + '.png'
        self.hangnum = self.hangnum + 1

    #  답지에 알파벳작성
    def updatecuslist(self, alpha):
        print("남은 LIFE ", "★"*(self.life-1))
        alpha = alpha.lower()
        x = 0
        idx = 0

        r = re.compile('[a-z]')
        match = r.search(alpha)
        if(match is None):
            print("영어만 입력하세요.")
            return False
        
        # 정답 내 모든 알파벳 찾기 위함
        while x != -1:

            x = self.answer.find(alpha)  # 단어 위치
            if x != -1:
                #  중복검사 방지
                self.answer = self.answer[0:x] + '_' + self.answer[x+1:]
                self.cusList[x] = alpha
                idx = idx + 1
        print(self.cusList)
        if idx == 0:
            #  알파벳이 포함되어 있지 않으면 life 깎기
            self.life = self.life - 1
            # 행걸 이미지 출력(1번부터 6번까지)
            self.sethanggirl()
            img = cv2.imread(self.hanggirl,0)
            cv2.namedWindow(self.hanggirl, cv2.WINDOW_NORMAL)
            cv2.imshow(self.hanggirl,img)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()


# 클래스 선언
an = BaseInfo()
st = StartGame()
pl = PlayGame()
sucess = False

# 게임 인트로
an.gameintro()


# 메뉴 선택
if an.subnum == '0':
    print("두 개의 주제 중 하나를 골라서 타이틀을 맞추는 게임입니다.")
    print("힌트를 보고 몇 글자의 알파벳인지 확인하세요.")
    print("목숨은 총 6개이며 틀릴 때마다 그림이 출력됩니다.")
    print(an.line)
    quit()
elif an.subnum == '1':
    an.setsubject("식당 방문")
    # 인사말
    print(an.subject + an.intro)
    print(an.line)
    # 식당 타이틀 세팅하기
    st.crawltofranchise()
elif an.subnum == '2':
    an.setsubject("영화 보기")
    # 인사말
    print(an.subject + an.intro)
    print(an.line)
    # 영화 타이틀 세팅하기
    st.crawltomovie()
elif an.subnum == '3':
    print("좋은 꿈 꾸세요^~^")
    print(an.line)
    quit()

#  게임 진행
pl.setanswer(st.answer)  
pl.setansList(st.ansList) 
pl.setcuslist(st.ansList)
# 사용자에게 알파벳 입력 받기
while pl.ansList != pl.cusList and pl.life > 0:
    print(an.line)
    pl.updatecuslist(input("> 알파벳입력 : "))
    print(an.line)

#  게임 결과
if pl.life == 0:
    print("게임에서 졌습니다.")
else:
    print("게임에서 이겼습니다.")