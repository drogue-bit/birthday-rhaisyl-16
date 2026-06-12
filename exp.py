from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

driver.get(
    "https://open.spotify.com/user/31junzitapcjrhhvlvg2ofuwwsey/recently-played-artists"
)

time.sleep(10)

html = driver.page_source

print(len(html))

with open("spotify.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()