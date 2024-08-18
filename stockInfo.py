import requests
from datetime import datetime,timedelta
import urllib3
import streamlit as st
import pandas as pd
import json



resultList = []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

authkey = 'bvaKtjYJhZTaGf%2FnaWnOgKRvWFZt90rfTuu1nUWwaVNqxTkJLWSrKT9oIw0AGoD5IiNaBUbdy%2BEgypnlZ%2ByZ6Q%3D%3D'

def timeCount(now, daybefore):
    return now - timedelta(days=daybefore)



def getStockInfo(baseDate):

    url = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={}&numOfRows=10000&resultType=json&basDt={}'.format(authkey,baseDate)
    r = requests.get(url, verify=False)
    if r.status_code == 200:

        data = r.json()

        length = len(data['response']['body']['items']['item'])

        cnt = 1
        for i in range(length):
            if (float(data['response']['body']['items']['item'][i]['fltRt']) > 29.7):
                # print(baseDate, data['response']['body']['items']['item'][i]['itmsNm'], data['response']['body']['items']['item'][i]['fltRt'])
                resultList.append([baseDate,data['response']['body']['items']['item'][i]['itmsNm'], data['response']['body']['items']['item'][i]['fltRt']])


def getCreditStatus():

    url = 'https://apis.data.go.kr/1160100/service/GetKofiaStatisticsInfoService/getGrantingOfCreditBalanceInfo?serviceKey=bvaKtjYJhZTaGf%2FnaWnOgKRvWFZt90rfTuu1nUWwaVNqxTkJLWSrKT9oIw0AGoD5IiNaBUbdy%2BEgypnlZ%2ByZ6Q%3D%3D&numOfRows=1&pageNo=1&resultType=json'
    r = requests.get(url, verify=False)
    if r.status_code == 200:
        data = r.json()
        print(data)
        # crdTrFingWhl 값 추출
        crdTrFingWhl_value = data['response']['body']['items']['item'][0]['crdTrFingWhl']
        print("crdTrFingWhl:", crdTrFingWhl_value)
        result = crdTrFingWhl_value[0:3]
        print("result : ", result)

        return result

now = datetime.now()
today = now.date()

for i in range(10, 0, -1):
    dTime = str(timeCount(now, i).date()).replace('-','')
    # print(dTime)
    getStockInfo(dTime)


frontData = pd.DataFrame(resultList, columns=['날짜', '종목명', '등락률'])
frontData.set_index('날짜', inplace=True)

col1, col2  = st.columns(2)

with col1:
    # now = datetime.now()
    # today = now.date()
    # for i in range(10, 0, -1):
    #     dTime = str(timeCount(now, i).date()).replace('-','')
    #     # print(dTime)
    #     getStockInfo(dTime)

    # frontData = pd.DataFrame(resultList, columns=['날짜', '종목명', '등락률'])
    # frontData.set_index('날짜', inplace=True)
    st.markdown("<h1 style='text-align: center; color: red;'>최근 상한가</h1>", unsafe_allow_html=True)
    st.table(frontData)

with col2:
    st.markdown("<h1 style='text-align: center; color: blue;'>신용잔고</h1>", unsafe_allow_html=True)
    result = getCreditStatus()
    jo = result[0:2]
    print(jo)
    uk = result[-1]
    print(uk)    
    # st.write("{}".format(getCreditStatus()))
    st.write(jo+"조", uk+"억")



# st.table(frontData)

