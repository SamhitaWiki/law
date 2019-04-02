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
main_url = "http://gujarathighcourt.nic.in/cjj"
image_url = "http://jkhighcourt.nic.in/"
link_url = "http://gujarathighcourt.nic.in/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html, context=context)
soup = BeautifulSoup(html, 'html.parser')

blocks = soup.find_all('div', attrs={'class': 'block-inner'})

blocks.pop(0)
blocks.pop(1)
del blocks[-1]
del blocks[-1]
del blocks[-4:]

details = blocks[0].find(
    'span', attrs={'class': 'subhead'})


profile = urllib2.Request(link_url, headers=hdr)
profile = urllib2.urlopen(profile, context=context)
profile = BeautifulSoup(profile, 'html.parser')

para = profile.find_all('p')


for block in blocks:
    img_src = block.find('img')['src']
    filename = "gujarat"+img_src.split('/')[-1].strip().encode("utf-8")
    fullname = block.find(
        'span', attrs={'class': 'highlight'}).get_text().strip().encode('utf-8')
    details = block.find(
        'span', attrs={'class': 'subhead'}).get_text().strip().encode('utf-8').split()
    dob = details[6]
    doj = details[15]
    link = block.find('a')['href']
    complete_link = link_url + link
    profile = urllib2.Request(complete_link, headers=hdr)
    profile = urllib2.urlopen(profile, context=context)
    profile = BeautifulSoup(profile, 'html.parser')

    para = profile.find_all('p')
    desc = para[0].get_text().strip().encode('utf-8')
    data.append((fullname, desc))
    r = requests.get(img_src)
    with open(filename, 'wb') as f:
        f.write(r.content)

with open('gujarat.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for fullname, desc in data:
        print fullname
        name = fullname.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, desc])
