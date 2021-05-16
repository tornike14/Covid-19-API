import requests
from tkinter import *
import json
import sqlite3

response = requests.get('https://disease.sh/v3/covid-19/all')
responseJson = response.json()

####
print(response.status_code)
print(response.content)
####
with open('data.json', 'w') as f1:
    json.dump(responseJson, f1, indent=4)
####
print(f"Total Cases:{responseJson['cases']} "
      f"Cases Today:{responseJson['todayCases']} "
      f"Total Deaths:{responseJson['deaths']} "
      f"Deaths Today:{responseJson['todayDeaths']} "
      f"Active Cases:{responseJson['active']}")
####
conn = sqlite3.connect('data.sqlite')
c = conn.cursor()

c.execute('''CREATE TABLE COVIDDATA(
    CASES_TOTAL CHAR(20) NOT NULL, CASES_TODAY CHAR(20),
    DEATHS_TOTAL CHAR(20), DEATHS_TODAY CHAR(20), CASES_ACTIVE CHAR(20) )''')

c.execute(
    f'INSERT INTO COVIDDATA (CASES_TOTAL, CASES_TODAY, DEATHS_TOTAL, DEATHS_TODAY, CASES_ACTIVE) VALUES (?, ?, ?, ?, ?)',
    (responseJson['cases'], responseJson['todayCases'], responseJson['deaths'], responseJson['todayDeaths'],
     responseJson['active']))

conn.commit()
conn.close()
