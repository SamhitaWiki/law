import sys
import os
import requests
import csv
from bs4 import BeautifulSoup
import urllib
import urllib2

data = []


main_url = "http://highcourt.cg.gov.in/sittingjudges/formarjudges.html"
image_url = "http://highcourt.cg.gov.in/sittingjudges/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html)
soup = BeautifulSoup(html, 'html.parser')

table = soup.find("table").find_all('tr')
print len(table)

for i in range(1, len(table)):
    rows = table[i].find_all('td')
    name = rows[1].find('font').get_text().strip()
    doj = rows[2].find('font').get_text().strip()
    dol = rows[3].find('font').get_text().strip()
    img_src = rows[4].find('img')['src']
    img_url = image_url + img_src
    filename = img_src.split('/')[-1]
    data.append((name, filename, doj, dol))
    print name
    r = requests.get(img_url)
    with open(filename, 'wb') as f:
        f.write(r.content)


with open('chattisgarh.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for fullname, filename, doj, dol in data:
        print fullname
        name = fullname.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, filename, doj, dol])
