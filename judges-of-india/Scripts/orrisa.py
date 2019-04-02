import ssl
import urllib2
import urllib
from bs4 import BeautifulSoup
import csv
import requests
import os
import sys
data = []


main_url = "http://www.orissahighcourt.nic.in/cjjudges.html"
image_url = "http://www.orissahighcourt.nic.in/"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html)
soup = BeautifulSoup(html, 'html.parser')
name_html = soup.find_all('div')[6]

name_html = name_html.find('table').find_all(
    'table')

i = 0
for table in name_html:
    if(i > 13):
        break
    table_data = table.find_all('td')
    name = table_data[2].get_text().encode('utf-8').strip()
    dob = table_data[4].get_text().encode('utf-8').strip()

    print i
    joining_date = table_data[6].get_text().encode('utf-8').strip()

    img_src = table_data[0].find('img')['src']
    img_url = image_url + img_src
    filename = img_src.split('/')[-1]

    r = requests.get(img_url)
    with open(filename, 'wb') as f:
        f.write(r.content)

    data.append((name, joining_date, filename, dob))
    i = i+1

with open('orrisa.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for name, join, filename, dob in data:
        print name
        name = name.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, join, filename, dob])
