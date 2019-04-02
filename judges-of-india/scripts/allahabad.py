import sys
import os
import requests
import csv
from bs4 import BeautifulSoup
import urllib
import urllib2

data = []


main_url = "http://allahabadhighcourt.in/Judges/ex-judge1991-2000.htm"
link_url = "http://allahabadhighcourt.in"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
html = urllib2.Request(main_url, headers=hdr)
html = urllib2.urlopen(html)
soup = BeautifulSoup(html, 'html.parser')

rows = soup.find('table', attrs={'class': 'withb'}).find_all('tr')

for i in range(3, len(rows)):
    coloumns = rows[i].find_all('td')
    if(coloumns[4].find('a') == None):
        desc = ""
        dob = ""
        fullname = coloumns[1].find('font').get_text().strip()
        print fullname
        filename = ""
    else:
        link = coloumns[4].find('a')['href']
        full_link = link_url + link
        link_page = urllib2.Request(full_link, headers=hdr)
        try:
            link_page = urllib2.urlopen(link_page)
        except urllib2.HTTPError as e:
            if e.code == 404:
                desc = ""
        else:
            link_page = BeautifulSoup(link_page, 'html.parser')
            fullname = coloumns[1].get_text().strip()
            print fullname
            details = link_page.find(
                'div', attrs={'class': 'Table'}).find_all('div')
            dob = details[8].get_text()
            print dob
            desc = ""
            filename = ""
            if(link_page.find('img') != None):
                img_src = link_page.find('img')['src']
                img_url = link_url + img_src
                filename = img_src.split('/')[-1]
                r = requests.get(img_url)
                with open(filename, 'wb') as f:
                    f.write(r.content)
    print fullname
    data.append((fullname, dob, filename))

with open('jharkhand.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)

    for fullname, dob, filename in data:
        writer.writerow([fullname, dob, filename])


"""
rows = soup.find('table', attrs={'class': 'withb'}).find_all('tr')

for i in range(3, len(rows)):
    coloumns = rows[i].find_all('td')
    if(coloumns[1].find('a') == None):
        fullname = coloumns[1].find('font').get_text().strip()
        desc = ""
    else:
        anchor = coloumns[1].find('a')
        fullname = anchor.get_text().strip()
        link = anchor['href']
        full_link = link_url + link
        link_page = urllib2.Request(full_link, headers=hdr)
        try:
            link_page = urllib2.urlopen(link_page)
        except urllib2.HTTPError as e:
            if e.code == 404:
                desc = ""
        else:
            link_page = BeautifulSoup(link_page, 'html.parser')
            desc = link_page.find('div').find('table').find_all('tr')[
                1].find('p').get_text()

    doj = coloumns[2].find('font')
    if(doj == None):
        doj = ""
    else:
        doj = doj.get_text()

    dol = coloumns[3].find('font')
    if(dol == None):
        dol = ""
    else:
        dol = dol.get_text()

    data.append((fullname, doj, dol, desc))
    print fullname
with open('allahabad.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for name, doj, dol, description in data:
        name = name.split()
        desc = description.split()
        if "Born" in desc:
            born_index = desc.index("Born")
        elif "born" in desc:
            born_index = desc.index("born")

        if "Born" in desc or "born" in desc:
            on_index = desc.index("on")
            print(on_index)
            if born_index == on_index - 1:
                dob_list = [desc[on_index+1],
                            desc[on_index+2], desc[on_index+3]]
                dob = " ".join(dob_list)
        else:
            dob = ""

        firstname = ' '.join(name[0:-1])
        print firstname
        lastname = name[-1]
        writer.writerow([description.encode("utf-8")])
"""
