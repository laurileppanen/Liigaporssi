import os
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import django
import sys
from django.conf import settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liigaporssi.settings")
django.setup()

DB_PATH = settings.DATABASES['default']['NAME']

URL = "https://liigaporssi.fi/sm-liiga/joukkueet/hifk/pelaajat"

URL2 = "https://liigaporssi.fi/sm-liiga"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(URL)
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.get(URL2 + "/sarjataulukko")
time.sleep(3)
soup2 = BeautifulSoup(driver.page_source, 'html.parser')

joukkueet = []
for td in soup2.find_all('td', class_='essential'):
    strong_tag = td.find('strong')
    if strong_tag:
        joukkue = strong_tag.get_text(strip=True)
        if not joukkue.isdigit():
            joukkueet.append(joukkue)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

for joukkue in joukkueet:
    taulun_nimi = f"{joukkue.replace('ä', 'a').replace('Ä', 'A').replace('-', '').replace(' ', '_')}_pelaajat"

    cursor.execute(f"DROP TABLE IF EXISTS {taulun_nimi}")
    
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {taulun_nimi} (
       pelaaja_id INTEGER PRIMARY KEY AUTOINCREMENT,
       nimi TEXT NOT NULL UNIQUE
    )
    ''')

    url_joukkue = joukkue.replace('ä', 'a').replace('Ä', 'A').lower()
    TEAM_URL = URL2 + f"/joukkueet/{url_joukkue}/pelaajat"
    driver.get(TEAM_URL)

    time.sleep(3)
    soup3 = BeautifulSoup(driver.page_source, 'html.parser')

    maalivahdit_taulukko = soup3.find('div', id=lambda x: x and x.startswith("stats_m_"))
    puolustajat_taulukko = soup3.find('div', id=lambda x: x and x.startswith("stats_p_"))
    hyokkaajat_taulukko = soup3.find('div', id=lambda x: x and x.startswith("stats_h_"))

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

    for nimi in maalivahdit:
      cursor.execute(f"INSERT OR IGNORE INTO {taulun_nimi} (nimi) VALUES (?)", (nimi,))

    for nimi in puolustajat:
      cursor.execute(f"INSERT OR IGNORE INTO {taulun_nimi} (nimi) VALUES (?)", (nimi,))

    for nimi in hyokkaajat:
      cursor.execute(f"INSERT OR IGNORE INTO {taulun_nimi} (nimi) VALUES (?)", (nimi,))    


driver.quit()
conn.commit()
conn.close()    