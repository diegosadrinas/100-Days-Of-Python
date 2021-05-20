from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

# data for BS
form_link = "https://docs.google.com/forms/d/e/1FAIpQLSeJavShRPLGC4b8T_rIJRrihNECm9tq9-Nfn0kx877-DNwjxQ/viewform?usp=" \
            "sf_link"
rental_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22" \
             "usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-" \
             "122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22" \
             "isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%" \
             "3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%" \
             "3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22" \
             "fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value" \
             "%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds" \
             "%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# request info
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Accept-Language": "es-xl",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

response = requests.get(rental_url, headers=headers)
rental_webpage = response.text

# scrap with bs
soup = BeautifulSoup(rental_webpage, "html.parser")


# get links
link_list = []
get_links = soup.select(".list-card-top a")
count_links = 0
for link in get_links:
    link = link["href"]
    if "http" in link:
        link_list.append(link)
    else:
        link_list.append(f"https://www.zillow.com{link}")
    count_links += 1

# get addresses
addresses_list = []
get_addresses = soup.find_all(class_="list-card-addr")
count_addresses = 0
for i in get_addresses:
    addresses_list.append(i.getText())
    count_addresses += 1

# get prices
prices_list = []
count_prices = 0
get_prices = soup.find_all(class_="list-card-price")
for i in get_prices:
    prices_list.append(i.getText())
    count_prices += 1

# check total amount of each data
print("Total prices:", count_prices)
print("Total addresses:", count_addresses)
print("Total links:", count_links)

# data for selenium
chrome_driver_path = "/Users/diegosadrinas/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeJavShRPLGC4b8T_rIJRrihNECm9tq9-Nfn0kx877-DNwjxQ/viewform"


# pass the data to the google form
for index in range(len(addresses_list)):
    print(addresses_list[index], prices_list[index], link_list[index])
    driver.get(google_form_url)
    time.sleep(2)
    address_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/'
                                                 'div/div[1]/input')
    price_input = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/'
                                               'div/div[1]/input')
    link_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/'
        'div[1]/input')
    address_input.send_keys(addresses_list[index])
    price_input.send_keys(prices_list[index])
    link_input.send_keys(link_list[index])
    submit_answer = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div').click()









