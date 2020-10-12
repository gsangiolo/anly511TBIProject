# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:17:48 2020

@author: sangi
"""

import requests

from bs4 import BeautifulSoup

response = requests.get('https://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate=&EndDate=&ILChkBx=yes&InjuriesChkBx=yes&submit=Search')
# will need to add &start=25,50,etc up to page 1560

text = response.text

soup = BeautifulSoup(text, 'html.parser')

tables = soup.find_all('table')

dataRows = []

for table in tables:
    #print(table)
    rows = table.find_all('tr')
    
    for row in rows:
        rowText = ''
        cells = row.find_all('td')
        for cell in cells:
            rowText += cell.text
        dataRows.append(rowText)