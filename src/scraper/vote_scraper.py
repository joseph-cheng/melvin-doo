from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options, executable_path="/usr/local/bin/geckodriver")

url = "https://app.capitoltrades.com/trades?page=1&pageSize=100"

driver.get(url)

# lol
time.sleep(2)

next_page_button = driver.find_elements_by_css_selector(".p-ripple .p-element .p-paginator-next .p-paginator-element .p-link")

print(next_page_button)

driver.quit()


