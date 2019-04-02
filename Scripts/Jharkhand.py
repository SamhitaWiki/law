import sys
import os
import requests
import csv
from bs4 import BeautifulSoup
import urllib
import urllib2

data = []


main_url = "https://jharkhandhighcourt.nic.in/retired-former-judges-high-court-jharkhand"
image_url = "https://jharkhandhighcourt.nic.in/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html)
soup = BeautifulSoup(html, 'html.parser')

virtual_page = soup.find('div', attrs={'class': 'field-item'}).find(
    'table').find_all('tr')

print virtual_page[11]
for i in range(0, 12, 2):

    image_rows = virtual_page[i].find_all('td')
    x = i + 1
    text_rows = virtual_page[x].find_all('td')

    for j in range(len(image_rows)):
        img_src = image_rows[j].find('img')['src']
        img_url = image_url + img_src
        filename = img_src.split('/')[-1].split('?')[0].encode('utf-8')
        fullname = text_rows[j].find('a')
        if(fullname == None):
            fullname = text_rows['a'].find(
                'p').get_text().encode('utf-8').strip()
        else:
            fullname = fullname.get_text().strip().encode("utf-8")
        data.append((fullname, filename))
        r = requests.get(img_url)
        with open(filename, 'wb') as f:
            f.write(r.content)


with open('jharkhand.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for fullname, filename in data:
        print fullname
        name = fullname.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, filename])
