from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

timeout = time.time() + 5
two_min = time.time() + 2 * 60

# Find elements
cookie = driver.find_element(By.ID, "cookie")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

try:
    while True:
        cookie.click()

        if time.time() > timeout:
            all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
            item_prices = []

            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)

            cookie_upgrades = {item_prices[n]: item_ids[n] for n in range(len(item_prices))}

            money = driver.find_element(By.ID, "money").text
            if "," in money:
                money = money.replace(",", "")
            cookie_count = int(money)

            affordable_upgrades = {cost: id for cost, id in cookie_upgrades.items() if cookie_count >= cost}

            if affordable_upgrades:
                highest_affordable = max(affordable_upgrades)
                print(f"Buying {highest_affordable}")
                to_purchase_id = affordable_upgrades[highest_affordable]
                driver.find_element(By.ID, to_purchase_id).click()

            timeout = time.time() + 5

        if time.time() > two_min:
            cookie_per_sec = driver.find_element(By.ID, "cps").text
            print(f"Cookies per second: {cookie_per_sec}")
            break

except KeyboardInterrupt:
    print("Bot Stopped")
