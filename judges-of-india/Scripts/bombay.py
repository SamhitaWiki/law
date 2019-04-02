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
main_url = "https://bombayhighcourt.nic.in/cjshow.php?auth=cGFnZW5vPTQ="
image_url = "https://bombayhighcourt.nic.in"
link_url = "https://bombayhighcourt.nic.in/"


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html, context=context)
soup = BeautifulSoup(html, 'html.parser')

form = soup.find('form', attrs={'name': 'cjnm'}).find_all('table')

table = soup.find('form', attrs={'name': 'cjnm'}).find_all('table')

url = form[3].find_all('a', attrs={'class': 'highlight'})
data_table = form[1]


urls = []

for i in range(3, len(url)):
    if(i < len(url)):
        urls.append(url[i]['href'].strip().encode('utf-8'))


def get_Data(form_data):

    img_src = form_data.find('img')['src'].replace('.', '', 1)
    img_url = image_url + img_src

    filename = img_src.split('/')[-1].strip()
    name = form_data.find(
        'td', attrs={'id': 'tdname'}).get_text().strip().encode('utf-8')

    timespan = form_data.find(
        'td', attrs={'class': 'timespan'}).get_text().strip().split("-")
    print timespan
    doj = timespan[0]
    if(len(timespan) > 1):
        dol = timespan[1]
    else:
        dol = ""
    desc = form_data.find(
        'td', attrs={'id': 'tdcontent'}).get_text().strip().encode('utf-8')

    data.append((name, doj, dol, desc, filename))
    print name
    """
    r = requests.get(img_url)
    with open(filename, 'wb') as f:
        f.write(r.content)
    """


def get_table(form_urls):
    for u in form_urls:
        main_url = link_url + u
        html = urllib2.Request(main_url, headers=hdr)
        html = urllib2.urlopen(html, context=context)
        soup = BeautifulSoup(html, 'html.parser')

        form = soup.find('form', attrs={'name': 'cjnm'}).find_all('table')

        table = soup.find('form', attrs={'name': 'cjnm'}).find_all('table')
        data_table = form[1]
        get_Data(data_table)


get_table(urls)

with open('bombay.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for name, doj, dol, desc, filename in data:
        print name
        name = name.split()
        firstname = ' '.join(name[0:-1])
        lastname = name[-1]
        writer.writerow([firstname, lastname, filename])
