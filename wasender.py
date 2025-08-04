import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os


class WASender:
    def wait_for_element(self, selector, content_amount):
        while len(self.driver.execute_script(f'return document.querySelectorAll("{selector}")')) < content_amount:
            time.sleep(0.1)

    def __init__(self, options: webdriver.ChromeOptions, driver_class = webdriver.Chrome, profile_path = os.path.join(os.getcwd(), 'profile')):
        if not os.path.exists(profile_path):
            os.mkdir(profile_path)

        options.add_argument("--incognito")

        self.driver = driver_class(options=options)
        self.accounts = {}

    def add_account(self, phone_number):
        self.driver.execute_script("window.open('https://web.whatsapp.com/')")

        next_window_index = self.driver.window_handles.index(self.driver.current_window_handle) + 1
        self.driver.switch_to.window(self.driver.window_handles[next_window_index])

        self.wait_for_element("#side", 1)

        self.accounts[phone_number] = self.driver.current_window_handle
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ESCAPE)

    def send_message(self, from_account: str, to_phone: str, text: str):
        if from_account not in self.accounts:
            self.add_account(from_account)

        self.driver.switch_to.window(self.accounts[from_account])
        self.driver.get(f"https://web.whatsapp.com/send?phone={to_phone}&text={text.replace(' ', '%20')}")

        self.wait_for_element("footer button", 3)
        self.driver.execute_script("document.querySelectorAll(\"footer button\")[2].click()")

    def quit(self):
        time.sleep(1)
        self.driver.quit()
