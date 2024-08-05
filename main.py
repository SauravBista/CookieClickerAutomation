from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Chrome options to keep the browser open after the script finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialize the Chrome driver and open the Cookie Clicker game website
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Set the initial timeout for checking upgrades and the total run time of the bot
timeout = time.time() + 5  # Check for upgrades every 5 seconds
two_min = time.time() + 2 * 60  # Run the bot for 2 minutes

# Find the cookie to click and the items in the store for potential upgrades
cookie = driver.find_element(By.ID, "cookie")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

try:
    while True:
        # Click the cookie
        cookie.click()

        # Check for affordable upgrades every 5 seconds
        if time.time() > timeout:
            all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
            item_prices = []

            # Extract the price of each upgrade item
            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)

            # Create a dictionary of item prices and their corresponding IDs
            cookie_upgrades = {item_prices[n]: item_ids[n] for n in range(len(item_prices))}

            # Get the current amount of cookies
            money = driver.find_element(By.ID, "money").text
            if "," in money:
                money = money.replace(",", "")
            cookie_count = int(money)

            # Find upgrades that are affordable with the current cookie count
            affordable_upgrades = {cost: id for cost, id in cookie_upgrades.items() if cookie_count >= cost}

            # Purchase the most expensive affordable upgrade
            if affordable_upgrades:
                highest_affordable = max(affordable_upgrades)
                print(f"Buying upgrade worth {highest_affordable} cookies")
                to_purchase_id = affordable_upgrades[highest_affordable]
                driver.find_element(By.ID, to_purchase_id).click()

            # Reset the timeout for the next upgrade check
            timeout = time.time() + 5

        # Check if the total run time has been reached
        if time.time() > two_min:
            # Print the cookies per second (CPS) rate and stop the bot
            cookie_per_sec = driver.find_element(By.ID, "cps").text
            print(f"Cookies per second: {cookie_per_sec}")
            break

except KeyboardInterrupt:
    print("Bot Stopped")
