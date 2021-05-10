from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time

chrome_driver_path = "/Users/diegosadrinas/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie_counter = driver.find_element_by_id("cookie")

# get ids for upgrades
upgrades_ids = driver.find_elements_by_css_selector("#store div")
ids_list = [item.get_attribute("id") for item in upgrades_ids]

# get prices for upgrades
all_prices = driver.find_elements_by_css_selector("#store b")
item_prices = []
for item in all_prices:
    element = item.text
    if element != "":
        cost = int(item.text.split("-")[1].strip().replace(",", ""))
        item_prices.append(cost)

prices_dict = {ids_list[i]: item_prices[i] for i in range(len(item_prices))}
print(prices_dict)

# time limit for playing and time delay for buying
time_out = time.time() + 60 * 5
delay_time_for_purchase = time.time() + 5

while time.time() < time_out:
    cookie_counter.click()
    try:
        if time.time() > delay_time_for_purchase:
            money = int(driver.find_element_by_id("money").text.replace(",", ""))

            # find affordable upgrades
            upgrades_to_buy = {}
            for upgrade_id, cost in prices_dict.items():
                if money > cost:
                    upgrades_to_buy[cost] = upgrade_id
            print(upgrades_to_buy)

            # pick the most expensive upgrade
            highest_price_id = max(upgrades_to_buy)
            print(highest_price_id)
            selected_upgrade = upgrades_to_buy[highest_price_id]
            print(selected_upgrade)
            buy_upgrade = driver.find_element_by_id(selected_upgrade)
            buy_upgrade.click()

            # update the delay time
            delay_time_for_purchase = time.time() + 5

    except StaleElementReferenceException as error:
        print(error)
        pass

cookies_per_sec = driver.find_element_by_id("cps").text
print(f"Your cookies per second ratio was {cookies_per_sec}")
driver.quit()
