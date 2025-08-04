import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os


class WASender:
    def wait_for_element(self, selector, content_amount):
        while len(self.driver.execute_script(f'return document.querySelectorAll("{selector}")')) < content_amount:
            time.sleep(0.1)

    def __init__(self, options: webdriver.ChromeOptions = webdriver.ChromeOptions(), driver_class = webdriver.Chrome, profile_path = os.getcwd()):
        if not os.path.exists(profile_path):
            os.mkdir(profile_path)

        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(f'user-data-dir={os.path.abspath(profile_path)}')
        options.add_argument('--profile-directory=Profile 1')
        options.add_argument('--profiling-flush=n')
        options.add_argument('--enable-aggressive-domstorage-flushing')

        self.driver = driver_class(options=options)
        self.driver.get("https://web.whatsapp.com/")
        self.wait_for_element("#side", 1)
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ESCAPE)
        time.sleep(1)

    def send_message(self, to_phone: str, text: str):
        self.driver.get(f"https://web.whatsapp.com/send?phone={to_phone}&text={text.replace(' ', '%20')}")
        self.wait_for_element("footer button", 3)
        self.driver.execute_script("document.querySelectorAll(\"footer button\")[2].click()")

    def quit(self):
        time.sleep(1)
        self.driver.quit()
