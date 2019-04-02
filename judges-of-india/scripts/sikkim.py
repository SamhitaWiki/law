import ssl
import urllib2
import urllib
from bs4 import BeautifulSoup
import csv
import requests
import os
import sys
data = []


main_url = "http://highcourtofsikkim.nic.in/hcs/formerchiefjustice"
image_url = "http://highcourtofsikkim.nic.in"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html)
soup = BeautifulSoup(html, 'html.parser')
name_html = soup.find_all('div', attrs={'class': 'panel-custom'})

names = name_html[0].find('div', attrs={
                          'class': 'panel-body'}).find_all('div')
names = names[1:]
desc = ""
for a in names:
    text = a.get_text().encode('utf-8')
    desc = desc + text


for a in name_html:
    desc = ""
    heading = a.find('div', attrs={'class': 'panel-heading'}
                     ).find('a').get_text().encode('utf-8').split()[0:-3]
    name = " ".join(heading)
    dates = a.find('strong').get_text().encode(
        'utf-8').replace("(", "").replace(")", "").split("to")
    img_src = a.find('div', attrs={
        'class': 'panel-body'}).find('img')['src']
    img_url = image_url + img_src

    filename = img_src.split('/')[-1]
    "Downloading images"
    r = requests.get(img_url)
    with open(filename, 'wb') as f:
        f.write(r.content)

    text = a.find('div', attrs={
        'class': 'panel-body'}).find_all('div')
    for b in text:
        new_text = b.get_text().encode('utf-8')
        desc = desc + new_text

    data.append((name, dates[0], dates[1], desc, filename))
    print name

with open('sikkim.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for name, join, leave, desc, filename in data:
        name = name.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, join, leave, desc, filename])
