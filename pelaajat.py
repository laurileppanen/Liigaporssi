from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://liigaporssi.fi/sm-liiga/joukkueet/hifk/pelaajat"
driver.get(url)    

time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

maalivahdit_taulukko = soup.find('div', id='stats_m_168761288')

maalivahti_nimi = maalivahdit_taulukko.find_all('td', class_='player_name essential persist')


maalivahdit =[]
for nimi in maalivahti_nimi:
    maalivahti = nimi.find('a', class_='player_link').text.strip()
    maalivahdit.append(maalivahti)

print(maalivahdit)