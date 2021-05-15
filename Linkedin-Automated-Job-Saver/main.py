from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from selenium import webdriver
import decouple
import time

USER_ID = decouple.config("USER_ID")
PASS = decouple.config("PASS")

linkedin_url = "https://www.linkedin.com/jobs/search/?currentJobId=2512331907&f_AL=true&f_E=2&f_WRA=true&geoId=" \
               "102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom"

chrome_driver_path = "/Users/diegosadrinas/Development/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.maximize_window()
driver.get(linkedin_url)
sign_in_button = driver.find_element_by_css_selector("a.nav__button-secondary")
sign_in_button.click()

username_input = driver.find_element_by_name("session_key")
password_input = driver.find_element_by_name("session_password")
username_input.send_keys(USER_ID)
password_input.send_keys(PASS)
sign_in_access = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
sign_in_access.click()
time.sleep(3)

job_containers = driver.find_elements_by_css_selector(".jobs-search-results__list-item")

application_number = 0
for item in job_containers:
    try:
        item.click()
        time.sleep(2)
        application_number += 1

        job_apply = driver.find_element_by_css_selector(".jobs-apply-button")
        job_apply.click()
        submit_application = driver.find_element_by_css_selector("footer button")
        if submit_application.text == "Siguiente":
            exit_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
            exit_button.click()
            time.sleep(1)
            confirm = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")
            confirm[1].click()
        else:
            submit_application.click()
    except ElementClickInterceptedException as new_window:
        driver.find_element_by_class_name("artdeco-modal__dismiss").click()
        print("An unexpected confirm dialog box was open. Dismiss and continue.")
        pass
    except NoSuchElementException as error:
        print(f"The button for applying a job is not available in application number :{application_number}. ")
        pass

driver.quit()
