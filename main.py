import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time


url = 'https://www.nba.com/stats/players/defense-dash-gt15'

driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))

driver.get(url)

selects = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9 ")
for select in selects:
    options = Select(select).options

for option in options:
    if option.text == 'All':
        option.click() # select() in earlier versions of webdriver
        break

# Find the table element
table = driver.find_element(By.CLASS_NAME, 'Crom_table__p1iZz')

# Find all rows in the table
rows = table.find_elements(By.TAG_NAME, 'tr')
defense_dash = []
i=0
# Loop through each row and extract the data from each cell
for row in rows:
    print(i)
    i+=1
    # Find all cells in the row
    cells = row.find_elements(By.TAG_NAME, 'td')

    # Loop through each cell and print the text
    for cell in cells:
            # If the cell does not have any child elements, print the text of the cell itself
            defense_dash.append(cell.text)
