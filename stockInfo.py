import requests
from datetime import datetime,timedelta
import urllib3
import streamlit as st
import pandas as pd

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

now = datetime.now()
today = now.date()

for i in range(10, 0, -1):
    dTime = str(timeCount(now, i).date()).replace('-','')
    # print(dTime)
    getStockInfo(dTime)



# print(resultList)

frontData = pd.DataFrame(resultList, columns=['날짜', '종목명', '등락률'])

# print(frontData)

st.table(frontData)
