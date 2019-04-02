import ssl
import urllib2
import urllib
from bs4 import BeautifulSoup
import csv
import requests
import os
import sys
data = []

main_url = "http://ghconline.gov.in/fcjusticesGHC.html"
image_url = "http://ghconline.gov.in/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html)
soup = BeautifulSoup(html, 'html.parser')
table = soup.find_all('table')[2]
name = table.find_all('b')
image = table.find_all('img')


for i in range(0, 31):
    img_src = image[i]['src']
    img_url = image_url + img_src
    filename = img_src.split('/')[-1]

    fullname = name[i].get_text()
    data.append((fullname, filename))

    r = requests.get(img_url)
    with open(filename, 'wb') as f:
        f.write(r.content)


with open('gauhati.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for fullname, filename in data:
        print fullname
        name = fullname.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, filename])
