from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus as qp
import ssl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 확인하고자 하는 날짜를 입력받음
date=input("\tEnter the date of the news you want to see ( ex) 2017-05-11) : ")
site1='https://datalab.naver.com/keyword/realtimeList.naver?datetime='+date+'T12:00:00'
site2='https://datalab.naver.com/keyword/realtimeList.naver?datetime='+date+'T20:00:00'

# https 관련 보안인증서 문제 해결 위한 코드
context = ssl._create_unverified_context()

# site1은 12시를 기준으로 잡고 site2는 저녁8시를 기준으로 잡음
html1 = urlopen(site1, context=context)
html2 = urlopen(site2, context=context)

# BeutifulSoup로 파싱하여 해당 날짜 오전,오후의 헤드라인 top5를 받아옴
soup1 = bs(html1, "html.parser")
soup2= bs(html2, "html.parser")

titles1 = soup1.find_all("span","title")
titles2 = soup2.find_all("span","title")

listtitle1=[]
listtitle2=[]

for title in titles1:
    listtitle1.append(title.text)
am1=listtitle1[-20];am2=listtitle1[-19];am3=listtitle1[-18];am4=listtitle1[-17];am5=listtitle1[-16];

for title in titles2:
    listtitle2.append(title.text)
pm1=listtitle2[-20];pm2=listtitle2[-19];pm3=listtitle2[-18];pm4=listtitle2[-17];pm5=listtitle2[-16];

#am1,am2...은 오전의 인기 검색어 1,2..위를 의미
#pm1,pm2...은 오후의 인기 검색어 1,2..위를 의미

listnew=[am1,am2,am3,am4,am5]
listref=[pm1,pm2,pm3,pm4,pm5]
for title in listref:
    if title not in listnew:
        listnew.append(title)
# 오전의 인기검색어를 기준으로 오전에는 없는 새로운 데이터를 listnew에 추가

#-------------

# listnew를 참조하여 headlines를 받아옴
# 해당 날짜의 인기검색어를 토대로 google news에서 해당 날짜 해당 검색어의 뉴스 헤드라인 받아옴
headlines=[]
parseDate = date.split('-')
y = parseDate[0]
m = parseDate[1]
d = parseDate[2]

print("\t탐색중...")
for title in listnew:
    url1 = 'https://www.google.co.kr/search?q='
    url2 = qp(title)
    url3 = '&source=lnt&tbs=cdr:1,cd_min:' + m + '/' + d + '/' + y + ',cd_max:' + m + '/' + d + '/' + y + '&tbm=nws'

    url = url1 + url2 + url3
    # print(url)

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req, context=context)
    htmlNews = response.read()
    soupNews = bs(htmlNews, 'html.parser')
    titleNews = soupNews.find_all('h3','r')[0].find('a').text
    headlines.append(titleNews)
    print("\t.......")
print()

# 검색어, 헤드라인 출력(아래 예시
# <성균관대>
# 성균관대학교 수시 논술 치뤄져
#
# <비트코인>
# 비트코인 ~~~~
# ...
print()
print("\t---헤드라인---")
for i in range(len(listnew)):
    print()
    print("\t<{0:s}>".format(listnew[i]))
    print("\t{0:s}".format(headlines[i]))


# 헤드라인 출력 후 옵션 제공(아래 예시)
# 1. 인기검색어 정보 제공
# 2. 인기검색어별 헤드라인 추가로 보기
# 3. 인기검색어별 당일 순위 그래프 보기
# 원하시는 기능을 선택하세요:
while True:
    func = 0

    while True:
        print()
        print("\t1. 인기검색어별 정보 제공")
        print("\t2. 인기검색어별 헤드라인 추가로 보기")
        print("\t3. 인기검색어별 당일 순위 그래프 보기")
        print("\t4. 헤드라인 다시 보기")
        print("\t0. 종료")
        func = int(input("\t원하시는 기능을 선택하세요: "))
        if 0 <= func <= 4:
            break
        else:
            print("\t잘못 입력하셨습니다.")
            continue

    if func == 0:
        print("\t종료합니다.")
        break;


    # 1번 선택시
    # 인기검색어 출력(아래 예시)
    # 1. 성균관대
    # 2. 비트코인
    # ...
    # 원하는 인기검색어를 선택하세요:
    # (출력 예시)
    # 성균관대는 ~~~~
    elif func == 1:
        print()
        for i in range(len(listnew)):
            print("\t{0:d}. {1:s}".format(i+1, listnew[i]))
        title = 0
        while True:
            title = int(input("\t정보를 원하는 타이틀을 선택해주세요: "))
            if 0 <= title <= len(listnew):
                break
            else:
                print('\t잘못 입력하셨습니다.')
                continue
        if title == 0:
            continue

        title = title-1

        print()
        print("\t<{0:s}>".format(listnew[title]))

        url1 = 'https://ko.wikipedia.org/wiki/'
        url2 = qp(listnew[title])

        url = url1+url2
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            response = urlopen(req, context=context)
            htmlNews = response.read()
            soupNews = bs(htmlNews, 'html.parser')
            info = soupNews.find_all('div','mw-parser-output')[0].find('p').text
            print("\t"+info)
        except:
            print("\t검색결과가 존재하지 않습니다.")


    # 2번 선택시
    # 인기검색어 출력(아래 예시)
    # 1. 성균관대
    # 2. 비트코인
    # ...
    # 원하는 인기검색어를 선택하세요
    # (출력 예시)
    # 성균관대 수시 논술 치뤄져
    # 성균관대 수시 논술 인원 ~~명
    # ...

    elif func == 2:
        print()
        for i in range(len(listnew)):
            print("\t{0:d}. {1:s}".format(i + 1, listnew[i]))
        title = 0
        while True:
            title = int(input("\t헤드라인을 보기 원하는 타이틀을 선택해주세요: "))
            if 0 <= title <= len(listnew):
                break
            else:
                print('\t잘못 입력하셨습니다.')
                continue
        if title == 0:
            continue

        title = title - 1

        n = int(input("\t원하는 헤드라인의 수를 입력해주세요: "))

        print()
        print("\t<{0:s}>".format(listnew[title]))

        url1 = 'https://www.google.co.kr/search?q='
        url2 = qp(listnew[title])
        url3 = '&source=lnt&tbs=cdr:1,cd_min:' + m + '/' + d + '/' + y + ',cd_max:' + m + '/' + d + '/' + y + '&tbm=nws'

        url = url1 + url2 + url3
        # print(url)

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req, context=context)
        htmlNews = response.read()
        soupNews = bs(htmlNews, 'html.parser')
        titleNews = soupNews.find_all('div','g')

        heads = []
        for subtitleNews in titleNews:
            for head in subtitleNews.find_all('a'):
                if len(head.text) < 10: continue
                heads.append(head.text)

        # print(soupNews.prettify())
        # print(titleNews)

        if len(heads) < n: n=len(heads)

        for i in range(n):
            print('\t'+heads[i])


    # 3번 선택시
    # 인기검색어 출력 및 선택(1,2번과 동일)
    # 검색어 순위 그래프 보여줌

    elif func == 3:
        print()
        for i in range(len(listnew)):
            print("\t{0:d}. {1:s}".format(i + 1, listnew[i]))
        title = 0
        while True:
            title = int(input("\t그래프를 보기 원하는 타이틀을 선택해주세요: "))
            if 0 <= title <= len(listnew):
                break
            else:
                print('\t잘못 입력하셨습니다.')
                continue
        if title == 0:
            continue

        title = title - 1
        titleT = listnew[title]

        timepicker = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        rank = []

        print()
        print("\t처리중")

        for i in range(24):

            url = 'https://datalab.naver.com/keyword/realtimeList.naver?datetime=' + date + 'T'+timepicker[i]+':00:00'
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(req, context=context)
            htmlNews = response.read()

            soup = bs(htmlNews, "html.parser")

            titles = soup.find_all("span", "title")

            listtitle = []
            newlist = []

            for title in titles:
                listtitle.append(title.text)

            for i in range(20):
                newlist.append(listtitle[-(20-i)])

            flag = 0
            for i in range(20):
                if titleT == newlist[i]:
                    flag=1
                    rank.append(i+1)
                    break

            if flag == 0:
                rank.append(21)

            print("\t.......")

        plt.gca().plot(range(1,25),rank)
        plt.gca().set_ylim([0,21])
        plt.gca().invert_yaxis()
        plt.show()

    elif func == 4:
        print()
        print("\t---헤드라인---")
        for i in range(len(listnew)):
            print()
            print("\t<{0:s}>".format(listnew[i]))
            print("\t{0:s}".format(headlines[i]))






