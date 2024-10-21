import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('liigaporssi.db')
cursor = conn.cursor()

url = 'https://liigaporssi.fi/sm-liiga/sarjataulukko'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    joukkueet = soup.find_all('td', class_='essential')
    print(joukkueet)

else: 
    print('hei')    

cursor.execute('''
CREATE TABLE IF NOT EXISTS Joukkueet (
    joukkue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nimi TEXT NOT NULL
)
''')

print("moooii")