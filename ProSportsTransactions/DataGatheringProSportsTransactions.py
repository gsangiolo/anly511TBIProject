# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 16:17:48 2020

@author: sangi
"""

import requests
import pandas as pd

from bs4 import BeautifulSoup

response = requests.get('https://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate=&EndDate=&ILChkBx=yes&InjuriesChkBx=yes&submit=Search')
# will need to add &start=25,50,etc up to page 1560

def scrapeAllProSportsFootballInjuries():
    url = 'https://www.prosportstransactions.com/football/Search/SearchResults.php?Player=&Team=&BeginDate=&EndDate=&ILChkBx=yes&InjuriesChkBx=yes&submit=Search'
    df = scrapeProSportsPageFromUrl(url)
    for i in range(2,1560):
        df = pd.concat([df, scrapeProSportsPageFromUrl(url + '&start=' + str((i-1)*25))])
    return df

def scrapeProSportsPageFromUrl(url):
    response = requests.get(url)
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    tables = soup.find_all('table')
    dataRows = []
    dates = []
    teams = []
    acquired = []
    relinquished = []
    notes = []
    for table in tables:
        #print(table)
        rows = table.find_all('tr')
        
        for row in rows:
            rowText = ''
            cells = row.find_all('td')
            for cell in cells:
                rowText += cell.text
            dataRows.append(rowText)
            if 'Date' not in cells[0].text and 'Previous' not in cells[1].text:
                dates.append(cells[0].text)
                teams.append(cells[1].text)
                acquired.append(cells[2].text)
                relinquished.append(cells[3].text)
                notes.append(cells[4].text)            
    df = pd.DataFrame(
        {'date': dates,
         'team': teams,
         'acquired': acquired,
         'relinquished': relinquished,
         'notes': notes
        })
    df.head(10)
    return df