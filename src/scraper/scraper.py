from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time

def strip_garbage(s):
    garbage = "<!---->"
    while s.startswith(garbage):
        s = s[len(garbage):]

    while s.endswith(garbage):
        s = s[:-len(garbage)]

    return s

def get_trades(driver):
    url = "https://app.capitoltrades.com/trades?page=1&pageSize=100"
    driver.get(url)
    # lol
    time.sleep(1)
    finished = False
    trades = []
    while not(finished):
        new_trades = get_trades_on_page(driver)
        trades += new_trades
        finished = not(get_next_page(driver))

    return trades
        




def get_trades_on_page(driver):
    table_elements = driver.find_elements_by_tag_name("app-table-template")
    table_size = 11
    counter = 0
    trades = []
    row = []
    for element in table_elements:
        if counter == 0:
            trades.append(row)
            row = []

        
        if counter == 10:
            pass
        else:

            text = ""

            inner_elements = element.find_elements_by_xpath(".//*")
            if len(inner_elements) > 0:
                for inner_element in element.find_elements_by_xpath(".//*"):
                    text += inner_element.get_attribute("innerHTML")

            else:
                text = element.get_attribute("innerHTML")
                text = strip_garbage(text)

            text = text.strip()
            text = text.replace("&amp;", "&")

            row.append(text)
        counter = (counter + 1) % table_size

    return trades


def get_next_page(driver):

    next_page_button = None
    while next_page_button == None:
        next_page_button = driver.find_element_by_class_name("p-paginator-next")
    print(next_page_button)

    button_classes = next_page_button.get_attribute("class").split()

    print(get_next_page.i)
    if "p-disabled" in button_classes:
        return False

    else:
        next_page_button.click()
        time.sleep(1)
        get_next_page.i += 1
        # lol
        return True

get_next_page.i = 0


options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options, executable_path="/usr/local/bin/geckodriver")
trades = get_trades(driver)
with open("trades.csv", "w+") as f:
    for trade in trades:
        line = ",".join(trade)
        f.write(line + "\n")


driver.quit()


