import requests
# import pymysql
import json
from bs4 import BeautifulSoup
import re

def  Item_price(ItemName,TransactionType):
    #物品名稱
    ItemName=ItemName
    #買或賣
    TransactionType=TransactionType

    url="https://www.ptt.cc/bbs/HardwareSale/index.html"
    headers={
            'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
            }#自定義直(網頁的headers
    Cookies={'over18':'1',}#自定義直(網頁的Cookies
    num_page = 10
    pttData = []
    Allcon=0


    for page in range(num_page):
        page = requests.get(url,headers=headers,cookies=Cookies).text  #把網頁變成text
        soup = BeautifulSoup(page,'lxml')
        controls = soup.select('.action-bar a.btn.wide ')
        for i in range(len(controls)):
            if(controls[i].text=='‹ 上頁'):
                url="https://www.ptt.cc"+str(controls[i].get('href'))
                title = soup.select('div.title>a')
                titledate = soup.select('div.meta>div.date')
                
                for j in range(len(title)):
                    # 使用正則表達式匹配 [賣/全國/皆可]
                    match_result = re.search(r'\['+TransactionType+'/[^]]+\].*'+ItemName+'.*',str( title[j].text))
                    time_result = str( titledate[j].text)
                    if match_result:
                        selling_info = match_result.group()
                        # print(selling_info+'   https://www.ptt.cc/'+str(title[j].get('href'))+" "+time_result)
                        Itemurl='https://www.ptt.cc/'+str(title[j].get('href'))
                        Itempage = requests.get(Itemurl,headers=headers,cookies=Cookies).text  #把網頁變成text
                        Itemsoup = BeautifulSoup(Itempage,'lxml')
                        #找特定
                        price_element = Itemsoup.find('span', class_='f3 hl', text='◎欲售價格：')
                        if price_element:
                            # 取得下一個兄弟元素的文字內容，這就是欲售價格
                            selling_price = price_element.find_next_sibling(text=True)
                            selling_price=selling_price.replace('(沒有明確價格、賣出後清空價格：水桶2m，售價高於原價：水桶1y+退文)', '').strip()
                            pttData.append({"title":selling_info,"URL":Itemurl,"Mon":selling_price,"tine":time_result})
                            Allcon=Allcon+1
    pttData.append({"Allcon":Allcon})
    print(pttData)
