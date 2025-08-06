import time
import os

from messageSender.sender import Sender
from messageSender import constants
from utils import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class WASender(Sender):
    def wait_for_element(self, selector, count):
        while len(self.driver.execute_script(f'return document.querySelectorAll(\'{selector}\')')) < count:
            time.sleep(0.1)

    def __init__(self, options: webdriver.ChromeOptions = webdriver.ChromeOptions(), driver_class = webdriver.Chrome, profile_path = os.path.join(os.getcwd(), "profile")):
        super().__init__()
        if not os.path.exists(profile_path):
            os.mkdir(profile_path)

        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(f'user-data-dir={os.path.abspath(profile_path)}')
        options.add_argument('--profile-directory=Profile 1')
        options.add_argument('--profiling-flush=n')
        options.add_argument('--enable-aggressive-domstorage-flushing')

        self.driver = driver_class(options=options)
        self.driver.get(constants.WA_URL)
        self.wait_for_element("#side", 1)
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ESCAPE)

        self.current = None

    def __go_to_user(self, to: str):
        if self.current is None or self.current != to:
            self.driver.get(f"{constants.SEND_URL}{to}")
        self.current = to

    def send(self) -> None:
        self.driver.execute_script("document.querySelectorAll(\"footer button\")[2].click();")

    def send_text(self, to: str, text: str):
        self.__go_to_user(to)
        self.wait_for_element("footer button", 3)
        self.driver.execute_script(
            f"const text = `{text}`;"
            "const dataTransfer = new DataTransfer();"
            "dataTransfer.setData('text', text);"
            "const event = new ClipboardEvent('paste', {"
            "  clipboardData: dataTransfer,"
            "  bubbles: true"
            "});"
            "document.querySelector('#main p').dispatchEvent(event);"
        )
        self.send()
        self.waiter()

    def quit(self):
        time.sleep(1)
        self.driver.quit()
    
    def send_image(self, to, image_path):
        self.__go_to_user(to)
        self.wait_for_element('[data-icon=\"plus-rounded\"]', 1)
        
        self.driver.execute_script("document.querySelector(\"[data-icon='plus-rounded']\").click()")
        count = self.driver.execute_script(
            'return document.querySelectorAll("span + div > span[data-icon=\'msg-dblcheck\']").length;'
        )
        self.driver.find_element(
            By.CSS_SELECTOR,
            'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
        ).send_keys(
            image_path
        )
        self.wait_for_element("div:has(+input) div[role=\"button\"]:has(> span > svg)", 2)
        self.driver.execute_script(
            'document.querySelectorAll("div:has(+input) div[role=\'button\']:has(> span > svg)")[1].click()'
        )
        self.wait_for_element('span + div > span[data-icon="msg-dblcheck"]', count)
        self.waiter()
        os.remove(image_path)

    @staticmethod
    def __await_func(wait_for: str) -> str:
        return " async function waiter(wait_for) {" \
        "     while (true) {" \
        "        let l = document.querySelectorAll(\"div[role='application'] div[role='row']\");" \
        "         let el = l[l.length - 1];" \
        "        if (el.querySelector(\"span+div>span[aria-hidden='false']\") === null) {await delay(); continue}" \
        "        let attr = el.querySelector(\"span+div>span[aria-hidden='false']\").getAttribute(\"data-icon\");" \
        "         if (wait_for === attr){" \
        "             return" \
        "         }" \
        "         await delay();" \
        "     }" \
        " };" \
        " function delay() {" \
        "     return new Promise((resolve, reject) => {" \
        "         setTimeout(() => {" \
        "            resolve("");" \
        "         }, 10);" \
        "     });" \
        " };" \
        f"await waiter(\"{wait_for}\");"
    
    def waiter(self):
        try:
            self.driver.execute_script(self.__await_func("msg-time"))
        except Exception as e:
            logger.collect_log(e)

        self.driver.execute_script(self.__await_func("msg-dblcheck"))
        time.sleep(0.1)