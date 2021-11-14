# Exchange Rate Program


# Package Loading

from PyQt5 import QtCore, QtWidgets, QtGui
import requests
from bs4 import BeautifulSoup as bs
import re


# Global Variable Declaration

food_total_txt = ''
housing_total_txt = ''
clothes_total_txt = '' 
transportation_total_txt = ''
personal_care_total_txt = ''
entertainment_total_txt = ''
rst = ''
obj_lst_2 = ['음료를 포함한 기본 점심 메뉴', '패스트푸드점의 세트 메뉴', '뼈 없는 닭가슴살 450g', '우유 1리터', '왕란 12개', '토마토 1kg', '치즈 450g', '사과 1kg', '감자 1kg', '맥주 500ml', '레드와인 한 병', '코카콜라 2L', '두 명 분의 빵 하루치', '비싼 지역의 25평 주택 임대료', '일반 지역의 25평 주택 임대료', '25평 주택의 2인 생활비(난방,전기,가스 등)', '비싼 지역의 13평 오피스 임대료', '일반 지역의 13평 오피스 임대료', '13평 오피스의 1인 생활비(난방,전기,가스 등)', '한달 인터넷 8mbps', '40인치 평면 TV', '전자레인지', '세제 3L', '청소 서비스', '청바지(리바이스 등) 한 벌', '여름 드레스(자라 등) 한 벌', '운동화(나이키,아디다스 등) 한 켤레', '남성 구두 한 켤레', '폭스바겐 골프 1.4 tsi 150cv 무옵션 한 대', '휘발유 1L', '대중교통 한 달 이용비', '감기약(타이레놀 등) 6일치', '항생제 한 박스(12다즈)', '개인 병원 의사 1회 방문', '탐폰 한 박스(32개)', '탈취제 50ml', '샴푸 400ml', '화장실 휴지 4롤', '치약 한 통', '남성 헤어 컷 가격', '2인분의 저녁 외식', '영화 티켓 두 장', '좋은 좌석의 극장 티켓 두 장', '2인분의 고급 이태리 식당 풀 코스', '칵테일 한 잔', '카푸치노 한 잔', '맥주 500ml', '아이패드 와이파이 128gb', '할인이 적용되지 않은 전화 요금 1분', '헬스장 한 달 이용권', '담배 한 갑']
url = 'https://finance.naver.com/marketindex/exchangeList.nhn'
comp_url = 'https://www.expatistan.com/cost-of-living/country/comparison/'
new_cou_eng = []
cou_eng = ['Cayman Islands', 'Hong Kong', 'Switzerland', 'Iceland', 'Bahamas', 'Norway', 'Singapore', 'Ireland', 'Qatar', 'Denmark', 'Israel', 'Luxembourg', 'New Zealand', 'United Kingdom', 'United States', 'Japan', 'United Arab Emirates', 'Finland', 'Australia', 'Netherlands', 'France', 'Lebanon', 'Sweden', 'Canada', 'Taiwan', 'Germany', 'Palestinian Territory', 'Mauritius', 'Belgium', 'South Korea', 'Austria', 'Puerto Rico', 'Italy', 'Bahrain', 'Oman', 'Malta', 'Cyprus', 'Trinidad and Tobago', 'Spain', 'Jamaica', 'Slovenia', 'Jordan', 'Uruguay', 'Costa Rica', 'Panama', 'Greece', 'Portugal', 'Estonia', 'Saudi Arabia', 'Latvia', 'Thailand', 'Croatia', 'Lithuania', 'Slovakia', 'China', 'Czech Republic', 'El Salvador', 'South Africa', 'Kenya', 'Chile', 'Brazil', 'Malaysia', 'Russia', 'Honduras', 'Botswana', 'Poland', 'Ecuador', 'Hungary', 'Indonesia', 'Guatemala', 'Mexico', 'Albania', 'Philippines', 'Dominican Republic', 'Peru', 'Serbia', 'Morocco', 'Bulgaria', 'Bolivia', 'Vietnam', 'Turkey', 'Uganda', 'Romania', 'Ukraine', 'Egypt', 'Bosnia and Herzegovina', 'Colombia', 'Nicaragua', 'Moldova', 'Azerbaijan', 'Kazakhstan', 'Algeria', 'Tanzania', 'Georgia', 'Paraguay', 'Tunisia', 'India']
cou_lst = ['케이맨 제도', '홍콩', '스위스', '아이슬란드', '바하마', '노르웨이', '싱가포르', '아일랜드', '카타르', '덴마크', '이스라엘', '룩셈부르크', '뉴질랜드', '영국', '미국', '일본', '아랍 에미리트', '핀란드', '호주', '네덜란드', '프랑스', '레바논', '스웨덴', '캐나다', '대만', '독일', '팔레스타인 영토', '모리셔스', '벨기에', '대한민국', '오스트리아', '푸에르토 리코', '이탈리아', '바레인', '오만', '몰타', '키프로스', '트리니다드 토바고', '스페인', '자메이카', '슬로베니아', '요르단', '우루과이', '코스타리카', '파나마', '그리스', '포르투갈', '에스토니아', '사우디 아라비아', '라트비아', '태국', '크로아티아', '리투아니아', '슬로바키아', '중국', '체코 공화국', '엘살바도르', '남아프리카', '케냐', '칠레', '브라질', '말레이시아', '러시아', '온두라스', '보츠와나', '폴란드', '에콰도르', '헝가리', '인도네시아', '과테말라', '멕시코', '알바니아', '필리핀 제도', '도미니카 공화국', '페루', '세르비아', '모로코', '불가리아', '볼리비아', '베트남', '터키', '우간다', '루마니아', '우크라이나', '이집트', '보스니아 헤르체고비나', '콜롬비아', '니카라과', '몰도바', '아제르바이잔', '카자흐스탄', '알제리', '탄자니아', '그루지야', '파라과이', '튀니지', '인도']
ind_lst = [] # Original Index


# Crawling with requests

res = requests.get(url)
text = res.text
soup = bs(text, 'html.parser')
lst = []
i = 0


# Data Preprocessing for 1st tap

for tr in soup.select('table.tbl_exchange > tbody > tr'):
    currency = tr.a.text
    currency = currency[:].strip()
    won = tr.select('td')[1].text
    buy_cash = tr.select('td')[2].text
    sell_cash = tr.select('td')[3].text 
    buy_send = tr.select('td')[4].text
    sell_send = tr.select('td')[5].text
    lst.append([currency,won,buy_cash,sell_cash,buy_send,sell_send])

for i in range(len(cou_eng)):
    new_cou_eng_text = cou_eng[i].replace(' ','-')
    new_cou_eng.append(new_cou_eng_text)

new_cou_lst = cou_lst[:]
cou_lst.sort()


# Variable initialization for GUI

app = None
Form = None
no_data = "데이터가 없습니다."

# PYQT5

class Ui_Form(object):

# GUI basic structure setting

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 511)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(lst))
        for i in range(len(lst)+1):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        for i in range(len(lst)):
            for v in range(len(lst[i])-1):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, v, item)
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.tab)
        self.comboBox.setObjectName("comboBox")
        for i in range(len(lst)):
            self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 0, 0, 1, 5)
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 2, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 2, 3, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 5)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 8, 1, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_4.addWidget(self.comboBox_2, 3, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_3.setObjectName("comboBox_3")
        for i in range(len(cou_lst)):
            self.comboBox_2.addItem("")
            self.comboBox_3.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_3, 3, 0, 1, 1)
        self.listView = QtWidgets.QListView(self.tab_3)
        self.listView.setObjectName("listView")
        self.gridLayout_4.addWidget(self.listView, 8, 0, 1, 1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout_4.addWidget(self.textBrowser_2, 8, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 7, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 7, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_4.addWidget(self.pushButton_2, 7, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 2, 0, 1, 3)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

# GUI detail settings

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "환율 어플리케이션"))
        self.label.setText(_translate("Form", "출처 : 네이버 금융"))
        for i in range(len(lst)):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Form" , lst[i][0]))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "기준 환율"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "살때_현금"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "팔때_현금"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "살때_송금"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "팔때_송금"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        for i in range(len(lst)):
            for v in range(len(lst[i])-1):
                item = self.tableWidget.item(i, v)
                item.setText(_translate("Form", lst[i][v+1]))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "환율 정보"))
        self.label_2.setText(_translate("Form", "단위 : \\"))
        self.lineEdit.setText(_translate("Form", "금액을 입력하세요."))
        for i in range(len(lst)):
            self.comboBox.setItemText(i, _translate("Form", lst[i][0]))
        self.pushButton.setText(_translate("Form", "환전"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "환율 계산기"))
        self.pushButton.clicked.connect(self.exchanger)
        self.pushButton.setShortcut(QtCore.Qt.Key_Return)
        for i in range(len(cou_lst)):
            self.comboBox_2.setItemText(i, _translate("Form", cou_lst[i]))
            self.comboBox_3.setItemText(i, _translate("Form", cou_lst[i]))
        self.label_9.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">▶</span></p></body></html>"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:9pt;\">출처 : https://www.expatistan.com/</span></p></body></html>"))
        self.label_11.setText(_translate("Form", "<html><head/><body><p align=\"center\">결과</p></body></html>"))
        self.label_10.setText(_translate("Form", "<html><head/><body><p align=\"center\">항목</p></body></html>"))
        self.pushButton_2.setText(_translate("Form", "비교하기"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\">비교할 국가를 선택해 주세요.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "물가 비교"))
        self.pushButton_2.clicked.connect(self.compare_country)

# Function of compare country(3rd tap)

    def compare_country(self, Form):
        self.textBrowser_2.clear()
        
        first_country = self.comboBox_2.currentText()
        second_country = self.comboBox_3.currentText()
        
        for i in range(len(cou_lst)):
            if first_country == new_cou_lst[i]:
                ind_num_1 = i
            if second_country == new_cou_lst[i]:
                ind_num_2 = i
        
        fir_cou = new_cou_eng[ind_num_1]
        sec_cou = new_cou_eng[ind_num_2]
        
        compared_url = comp_url + fir_cou + '/' + sec_cou
        
        res1 = requests.get(compared_url)
        text1 = res1.text
        soup1 = bs(text1, 'html.parser')
        
        compared_rst = soup1.select('#content > div > div:nth-child(5) > div:nth-child(1)')[0].h1.text
        compared_rst = compared_rst[:].strip()
        
        global rst
        
        if 'cheaper' in compared_rst:
            comp_num = re.findall("\d+", compared_rst)
            rst = "'" + second_country + "'의 물가는 '" + first_country + "' 보다 " + comp_num[0] + '% 더 싼 편 입니다.'
        elif 'expensive' in compared_rst:
            comp_num = re.findall("\d+", compared_rst)
            rst = "'" + second_country + "'의 물가는 '" + first_country + "' 보다 " + comp_num[0] + '% 더 비싼 편 입니다.'
        elif 'same' in compared_rst:
            rst = second_country + ' 와(과) ' + first_country + '은(는) 물가가 거의 비슷한 편입니다.'
        
        ans_lst = []
        obj_lst = ['음식','주거','의류','교통','위생','오락']
        
        for i in range(6):
            
            str_1 = soup1.select('#tr_{}'.format(i+1))[0].text.strip()
            if '+' in str_1:
                str_1 = obj_lst[i] + ' + ' + (str(re.findall("\d+", str_1)[0])) + "%"
            elif '-' in str_1:
                str_1 = obj_lst[i] + ' - ' + (str(re.findall("\d+", str_1)[0])) + "%"
            else:
                str_1 = obj_lst[i] + ' 0%'
            ans_lst.append(str_1)
        
        str_1 = soup1.select('#content > div > div.block.first.comparison > div.prices > table > tfoot > tr')[0].text.strip()

        if '+' in str_1:
            str_1 = '총합 + ' + (str(re.findall("\d+", str_1)[0])) + "%"
        elif '-' in str_1:
            str_1 = '총합 - ' + (str(re.findall("\d+", str_1)[0])) + "%"
        else:
            str_1 = '총합 0%'

        ans_lst.append(str_1)
        self.textBrowser_2.append(rst)
        
        self.model = QtGui.QStandardItemModel()
        
        for f in ans_lst:
            self.model.appendRow(QtGui.QStandardItem(f))
        
        self.listView.setModel(self.model)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.clicked[QtCore.QModelIndex].connect(self.setListView)
        
        i = 0
        lst_1 = []
        lst_2 = []

        while(True):
            if (i <= 16 and i >= 4) or (i <= 30 and i >= 20) or (i <= 37 and i >= 34) or (i <= 43 and i >= 41) or (i <= 55 and i >= 47) or (i <= 69 and i >= 59):
                a = soup1.select('#content > div > div.block.first.comparison > div.prices > table > tbody > tr:nth-child({}) > td.price.city-2'.format(i))
                a = a[0].text.strip().replace('\n','')
                a = a.replace(' ','')
                lst_1.append(a)
                b = soup1.select('#content > div > div.block.first.comparison > div.prices > table > tbody > tr:nth-child({}) > td.price.city-1'.format(i))
                b = b[0].text.strip().replace('\n','')
                b = b.replace(' ','')
                lst_2.append(b)
            i += 1
            if i > 69:
                break
            
        global food_total_txt
        food_total_txt = ''
        
        global housing_total_txt
        housing_total_txt = ''
        
        global clothes_total_txt
        clothes_total_txt = ''
        
        global transportation_total_txt
        transportation_total_txt = ''
        
        global personal_care_total_txt
        personal_care_total_txt = ''
        
        global entertainment_total_txt
        entertainment_total_txt = ''
        
        for i in range(13):
            food_txt = obj_lst_2[i] + '\n' + first_country + ' : ' + lst_2[i] + '\n' + second_country + ' : ' + lst_1[i] + '\n\n'
            food_total_txt += food_txt
        
        for i in range(13,24):
            housing_txt = obj_lst_2[i] + '\n' + first_country + ' : ' + lst_2[i] + '\n' + second_country + ' : ' + lst_1[i] + '\n\n'
            housing_total_txt += housing_txt
        
        for i in range(24,28):
            clothes_txt = obj_lst_2[i] + '\n' + first_country + ' : ' + lst_2[i] + '\n' + second_country + ' : ' + lst_1[i] + '\n\n'
            clothes_total_txt += clothes_txt
        
        for i in range(28,31):
            transportation_txt = obj_lst_2[i] + '\n' + first_country + ' : ' + lst_2[i] + '\n' + second_country + ' : ' + lst_1[i] + '\n\n'
            transportation_total_txt += transportation_txt
        
        for i in range(31,40):
            personal_care_txt = obj_lst_2[i] + '\n' + first_country + ' : ' + lst_2[i] + '\n' + second_country + ' : ' + lst_1[i] + '\n\n'
            personal_care_total_txt += personal_care_txt
            
        for i in range(40,51):
            entertainment_txt = obj_lst_2[i] + '\n' + first_country + ' : ' + lst_2[i] + '\n' + second_country + ' : ' + lst_1[i] + '\n\n'
            entertainment_total_txt += entertainment_txt
        

# Function of filling textBrowswer in price comparison UI(3rd tap)

    def setListView(self, index):
        self.textBrowser_2.clear()
        item = self.model.itemFromIndex(index)
        it_ind = item.index().row()
        if it_ind == 0:
            self.textBrowser_2.append(food_total_txt)
        elif it_ind == 1:
            self.textBrowser_2.append(housing_total_txt)
        elif it_ind == 2:
            self.textBrowser_2.append(clothes_total_txt)
        elif it_ind == 3:
            self.textBrowser_2.append(transportation_total_txt)
        elif it_ind == 4:
            self.textBrowser_2.append(personal_care_total_txt)
        elif it_ind == 5:
            self.textBrowser_2.append(entertainment_total_txt)
        else:
            self.textBrowser_2.append(rst)
    
# Function of exchanger(2nd tap)

    def exchanger(self, Form):
        self.textBrowser.clear()
        ex_lst = []
        ex_lst1 = []
        str1 = self.comboBox.currentText()
        for i in range(len(lst)):
            if str1 == lst[i][0]:
                ex_lst = lst[i]
        try:
            won = float(self.lineEdit.text())
        except ValueError:
            self.textBrowser.append("숫자를 입력해 주세요.")
        else:
            for i in range(len(ex_lst)-1):
                copied = ex_lst[i+1][:]
                copied = copied.replace("," , "")
                ex_lst1.append(float(copied))
            try:
                rate1 = round((won / ex_lst1[0]) , 2)
            except ZeroDivisionError:
                rate1 = no_data
            try:
                buy_cash1 = round((won / ex_lst1[1]) , 2)
            except ZeroDivisionError:
                buy_cash1 = no_data
            try:
                sel_cash1 = round((won / ex_lst1[2]) , 2)
            except ZeroDivisionError:
                sel_cash1 = no_data
            try:
                buy_send1 = round((won / ex_lst1[3]) , 2)
            except ZeroDivisionError:
                buy_send1 = no_data
            try:
                sel_send1 = round((won / ex_lst1[4]) , 2)
            except ZeroDivisionError:
                sel_send1 = no_data
            output = str("기준 환율 : " + str(rate1) + "\n살때_현금 : " + str(buy_cash1) + "\n팔때_현금 : " + str(sel_cash1) + "\n살때_송금 : " + str(buy_send1) + "\n팔때_송금 : " + str(sel_send1))
            self.textBrowser.append(output)


# Main function

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    app.exec_()
    del app
    del Form

# Created by Jihyun Jung