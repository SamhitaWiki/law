import urllib2
import urllib
from bs4 import BeautifulSoup
import csv
import requests
import os
import ssl
import sys

data = []

context = ssl._create_unverified_context()
main_url = "http://meghalayahighcourt.nic.in/former-cj-judges"
image_url = "http://jkhighcourt.nic.in/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html, context=context)
soup = BeautifulSoup(html, 'html.parser')


tables = soup.find_all(
    'div', attrs={'class': 'table-responsive'})[2].find_all('tr')[1:]

for table in tables:
    table_data = table.find_all('td')
    details = table_data[0].get_text().split()
    name = " ".join(details[0:-3])
    dates = " ".join(details[-3:-1])
    dates = dates.split("to")
    doj = dates[0]

    img_src = table_data[1].find('img')['src']
    filename = img_src.split('/')[-1]
    data.append((name, filename, doj))

    r = requests.get(img_src, verify=False)
    with open(filename, 'wb') as f:
        f.write(r.content)

with open('megh.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for fullname, filename, doj in data:
        print fullname
        name = fullname.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname.encode('utf-8'),
                         lastname.encode('utf-8'), filename, doj])
