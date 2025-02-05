from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import sqlite3

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://liigaporssi.fi/sm-liiga/joukkueet/hifk/pelaajat"
driver.get(url)    

time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

maalivahdit_taulukko = soup.find('div', id='stats_m_168761288')
puolustajat_taulukko = soup.find('div', id='stats_p_168761288')
hyokkaajat_taulukko = soup.find('div', id='stats_h_168761288')

maalivahti_nimi = maalivahdit_taulukko.find_all('td', class_='player_name essential persist')
puolustajat_nimi = puolustajat_taulukko.find_all('td', class_='player_name')
hyokkaajat_nimi = hyokkaajat_taulukko.find_all('td', class_='player_name')

maalivahdit =[]
for nimi in maalivahti_nimi:
    maalivahti = nimi.find('a', class_='player_link').text.strip()
    maalivahdit.append(maalivahti)

puolustajat = []
for nimi in puolustajat_nimi:
    puolustaja = nimi.find('a', class_='player_link').text.strip()
    puolustajat.append(puolustaja)

hyokkaajat = []
for nimi in hyokkaajat_nimi:
    hyokkaaja = nimi.find('a', class_='player_link').text.strip()
    hyokkaajat.append(hyokkaaja)


print('MOKET:', maalivahdit)
print('PUOLUSTAJAT:', puolustajat)
print('HYÖKKÄÄJÄT:', hyokkaajat)


conn = sqlite3.connect('liigaporssi.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Pelaajat (
    pelaaja_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nimi TEXT NOT NULL,
    pelipaikka TEXT NOT NULL,
    Joukkue_id INTEGER,
    FOREIGN KEY (joukkue_id) REFERENCES Joukkueet(joukkue_id),
    UNIQUE(nimi, joukkue_id)                                                                      
)
''')

cursor.execute("SELECT joukkue_id FROM Joukkueet WHERE nimi = ?", ("HIFK",))
joukkue_id = cursor.fetchone()[0]

for nimi in maalivahdit:
    cursor.execute("INSERT OR IGNORE INTO Pelaajat (nimi, pelipaikka, joukkue_id) VALUES (?, ?, ?)", (nimi, "Maalivahti", joukkue_id))

for nimi in puolustajat:
    cursor.execute("INSERT OR IGNORE INTO Pelaajat (nimi, pelipaikka, joukkue_id) VALUES (?, ?, ?)", (nimi, "Puolustaja", joukkue_id))

for nimi in hyokkaajat:
    cursor.execute("INSERT OR IGNORE INTO Pelaajat (nimi, pelipaikka, joukkue_id) VALUES (?, ?, ?)", (nimi, "Hyökkääjä", joukkue_id))

conn.commit()
conn.close()

 