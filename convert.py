import re


def converttotitle(originTitle):  # 정규표현식을 통해 타이틀 획득
    title = re.sub('[0-9-=+,#/|?:^$.@*\()"]', '', originTitle)  # 특수문자 및 숫자 제거
    title = re.sub('^[\s]', '', title)  # 맨 앞 공백 제거
    title = re.sub('[\s]$', '', title)  # 맨 뒤 공백 제거

    c = re.search("([a-zA-Z]*(\s|')*)*", title)  # 정규표현식에 맞게 title 가져오기
    if c == None:
        return None
    else:
        return str(c.group())