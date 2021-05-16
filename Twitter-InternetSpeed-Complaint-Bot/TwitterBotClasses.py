from selenium import webdriver
import decouple
import time


class InternetSpeedTwitterBot:
    def __init__(self):
        self.chrome_driver_path = decouple.config("CHROME_DRIVER_PATH")
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
        self.current_speed = None
        self.speed_up = 200

    def get_internet_speed(self):
        speed_url = "https://fast.com"
        driver = self.driver
        driver.get(speed_url)
        time.sleep(14)
        self.current_speed = driver.find_element_by_id("speed-value").text
        return int(self.current_speed)

    def tweet_internet_company(self):
        driver = self.driver
        url = "https://twitter.com/login"
        driver.get(url)
        user_id = decouple.config("USER_ID")
        password = decouple.config("PASSWORD")
        time.sleep(2)
        username_input = driver.find_element_by_xpath('//input[contains(@name,"username")]').send_keys(user_id)
        password_input = driver.find_element_by_xpath('//input[@name="session[password]"]').send_keys(password)
        login = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/'
                                                  'div[3]/div').click()
        time.sleep(4)
        text_box = driver.find_element_by_class_name("public-DraftStyleDefault-ltr")
        text_box.click()
        tweet_input = text_box.send_keys(f"@iplanliv mi velocidad de bajada en este momento es de {self.current_speed}, "
                                         f"cuando estoy pagando por {self.speed_up}mb, Cómo lo solucionamos??")
        send_tweet = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/'
                                                  'div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]'
                                                  '/div[3]/div')
        send_tweet.click()
