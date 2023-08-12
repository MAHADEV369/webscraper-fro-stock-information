import requests
from bs4 import BeautifulSoup
import time
import csv
import mail_report
from datetime import date


urls = ["https://finance.yahoo.com/quote/IBM?p=IBM&.tsrc=fin-srch", "https://finance.yahoo.com/quote/GOOG?p=GOOG&.tsrc=fin-srch","https://finance.yahoo.com/quote/MTP?p=MTP&.tsrc=fin-srch"]

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

today = str(date.today()) + ".csv"
csv_file = open(today,"w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Stock name','Current price','Previous Close','Open','Bid','Ask','Day Range','52 Week Range','Volume','Avg. Volume	'])


for url in urls:
    stock = []
    html_page = requests.get(url,headers=headers)

    #print (html_page.content)

    soup = BeautifulSoup(html_page.content,'lxml')

    header_info = soup.find_all("div",id="quote-header-info")[0]
    stock_title = header_info.find("h1").get_text()
    current_price = header_info.find("div",class_="My(6px) Pos(r) smartphone_Mt(6px)").find("span").get_text()
    #print(stock_title)
    #print(current_price)
    stock.append(stock_title)
    stock.append(current_price)


    table_info = soup.find_all("div",class_="D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)" )[0].find_all("tr")

    for i in range(0,8):
        #heading = table_info[i].find_all("td")[0].get_text()
        value = table_info[i].find_all("td")[1].get_text()
        #print(heading+ " : " +value)
        stock.append(value)
        
    csv_writer.writerow(stock)
    time.sleep(2)    
csv_file.close()
mail_report.send(filename=today)