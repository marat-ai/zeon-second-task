import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, date

response = requests.get("https://www.akchabar.kg/ru/exchange-rates/")
soup = BeautifulSoup(response.text, 'html.parser')

dt = dict()
lst = list()

table_data = soup.find(id='rates_table')
body = table_data('tbody')

tr = body[0].find_all('tr')
all_data_lst = list()
for t in tr:
    banks_lst = list()
    ls = list()
    exc_rate_lst = list()

    title = t.find('a')['title'].split('.')
    bank = title[0]
    if len(bank.split()) >= 3:
        bank = t.find('a').text
    banks_lst.append(bank)

    exc_rate = t.find_all('td')
    for element in exc_rate:
        element = element.text
        exc_rate_lst.append(element)
    ls = exc_rate_lst[1:]
    for l in ls:
        banks_lst.append(l.strip())

    date = t.find('a')['title'].split('в:')
    banks_lst.append(date[-1])
    all_data_lst.append(banks_lst)

head_lst = list('#')
head = table_data('thead')
head_th = head[0].find_all('th')

# head_th = head_tr.find
h = 0
for t in head_th:
    if h == 0 :
        sp = t.find('span').text
        head_lst.append(sp)
    else:
        di = t.find('div')
        sp = di.find('span').text
        # sp = img['alt']
        head_lst.append(sp)
        head_lst.append(sp)

    h+=1

print(head_lst)

c = 0
now = datetime.now()
current_time = now.strftime("%d%m%Y%H%M%S")

fname = 'data' + str(current_time) + '.csv'
with open(fname, 'w', newline='') as csv_file:
    thewriter = csv.DictWriter(csv_file, fieldnames=head_lst)
    thewriter.writeheader()

    for bank in all_data_lst:
        c += 1
        thewriter.writerow({head_lst[0]:c, head_lst[1]:bank[0], head_lst[2]:bank[1], head_lst[3]:bank[2], head_lst[4]:bank[3], head_lst[5]:bank[4], head_lst[6]:bank[5], head_lst[7]:bank[6], head_lst[8]:bank[8], head_lst[9]:bank[9]})

print(all_data_lst)
