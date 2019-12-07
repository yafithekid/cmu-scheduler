#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 10:40:05 2019

@author: sidd
"""

import requests 
from bs4 import BeautifulSoup
import pandas as pd

with open("94.txt", "r", encoding  = "windows-1252") as f:
    
    contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')
    '''
    table = soup.find(id = "search-results-table")
    
    table.findAll('table')[0].tbody.findAll('tr')

    
    print(names)
    '''
    #https://datascience.stackexchange.com/questions/10857/how-to-scrape-a-table-from-a-webpage
    table_body=soup.find('tbody')
    rows = table_body.find_all('tr')
    d = {"Course":[], "Course Title":[], "Units":[], "Sec":[], "Mini":[], "Days":[], 
         "Begin":[] , "End":[], "Teaching Location":[], "BDLG/Room":[], "Instructor":[]}
    df = pd.DataFrame(d)

    for row in rows:
        cols=row.find_all('td')
        cols=[x.text.strip() for x in cols]
        df = df.append({'Course':cols[0],'Course Title':cols[1], 'Units': cols[2], 'Sec':cols[3], 
                        'Mini':cols[4], 'Days':cols[5], 'Begin':cols[6], 'End':cols[7], 'Teaching Location':cols[8],
                        'BDLG/Room':cols[9], 'Instructor':cols[10]}, ignore_index = True)
    print(df['Course'])
    df.to_csv('94.csv', index = False)
    
