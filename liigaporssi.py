import sqlite3
import requests
from bs4 import BeautifulSoup

conn = sqlite3.connect('liigaporssi.db')
cursor = conn.cursor()

url = 'https://liigaporssi.fi/sm-liiga/sarjataulukko'

response = requests.get(url)

if response.status_code != 200:
    print(f"Pyyntö epäonnistui, virhekoodi: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')
joukkueet = []

for td in soup.find_all('td', class_='essential'):
    strong_tag = td.find('strong')
    if strong_tag:
        joukkue = strong_tag.get_text(strip=True)
        if not joukkue.isdigit():
            joukkueet.append(joukkue)

print('JOUKKUEET:', joukkueet)

cursor.execute('''
CREATE TABLE IF NOT EXISTS Joukkueet (
    joukkue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nimi TEXT NOT NULL
)
''')

for joukkue in joukkueet:
    cursor.execute('INSERT OR IGNORE INTO Joukkueet (nimi) VALUES (?)', (joukkue,))

conn.commit()
conn.close()

 