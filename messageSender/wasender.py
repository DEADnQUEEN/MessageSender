import asyncio
import time
import os

from messageSender.sender import Sender
from messageSender import constants
from utils import logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class WASender(Sender):
    async def await_for_element(self, selector, count) -> bool:
        save_wait = 60 * 10
        while len(self.driver.execute_script(f'return document.querySelectorAll(\'{selector}\')')) < count and save_wait > 0:
            await asyncio.sleep(0.1)
            save_wait = save_wait - 1

        return save_wait > 0

    def wait_for_element(self, selector, count) -> bool:
        save_wait = 60 * 10
        while len(self.driver.execute_script(f'return document.querySelectorAll(\'{selector}\')')) < count and save_wait > 0:
            time.sleep(0.1)
            save_wait = save_wait - 1

        return save_wait > 0

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

        if not self.wait_for_element("#side", 1):
            raise ValueError

        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ESCAPE)

        self.current = None

    def __go_to_user(self, to: str):
        if self.current is None or self.current != to:
            self.driver.get(f"{constants.SEND_URL}{to}")
        self.current = to

    def send(self) -> None:
        self.driver.execute_script("document.querySelectorAll(\"footer button\")[2].click();")

    def paste_text(self, text):
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

    def send_text(self, to: str, text: str) -> bool:
        self.__go_to_user(to)

        if not self.wait_for_element("footer button", 3):
            logger.collect_log(f"text is not sended for {to}")
            return False

        self.paste_text(text)
        self.send()

        self.waiter()
        return True

    async def a_send_text(self, to, text) -> bool:
        self.__go_to_user(to)

        if await self.await_for_element("footer button", 3):
            logger.collect_log(f"text is not sended for {to}")
            return False

        self.paste_text(text)
        self.send()

        self.waiter()
        return True


    def quit(self):
        time.sleep(1)
        self.driver.quit()
    
    def send_image(self, to, image_path):
        self.__go_to_user(to)

        if not self.wait_for_element('[data-icon=\"plus-rounded\"]', 1):
            logger.collect_log(f"image {image_path} not sended for {to}")
            return False
        
        self.driver.execute_script("document.querySelector(\"[data-icon='plus-rounded']\").click()")

        self.driver.find_element(
            By.CSS_SELECTOR,
            'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
        ).send_keys(
            image_path
        )

        if not self.wait_for_element("div:has(+input) div[role=\"button\"]:has(> span > svg)", 2):
            logger.collect_log(f"image {image_path} not sended for {to}")
            return False

        self.driver.execute_script(
            'document.querySelectorAll("div:has(+input) div[role=\'button\']:has(> span > svg)")[1].click()'
        )

        self.waiter()
        os.remove(image_path)
        return True

    async def a_send_image(self, to, image_path) -> bool:
        self.__go_to_user(to)

        if not await self.await_for_element('[data-icon=\"plus-rounded\"]', 1):
            logger.collect_log(f"image {image_path} not sended for {to}")
            return False

        self.driver.execute_script("document.querySelector(\"[data-icon='plus-rounded']\").click()")

        self.driver.find_element(
            By.CSS_SELECTOR,
            'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
        ).send_keys(
            image_path
        )

        if not await self.await_for_element("div:has(+input) div[role=\"button\"]:has(> span > svg)", 2):
            logger.collect_log(f"image {image_path} not sended for {to}")
            return False

        self.driver.execute_script(
            'document.querySelectorAll("div:has(+input) div[role=\'button\']:has(> span > svg)")[1].click()'
        )

        self.waiter()
        os.remove(image_path)
        return True

    def __await_func(self, waits_for: list[str]) -> bool:
        function_text =  " async function waiter(waits_for) {" \
        "     while (true) {" \
        "        let l = document.querySelectorAll(\"div[role='application'] div[role='row']\");" \
        "        let el = l[l.length - 1];" \
        "        if (el.querySelector(\"span+div>span[aria-hidden='false']\") === null) {await delay(); continue}" \
        "        let attr = el.querySelector(\"span+div>span[aria-hidden='false']\").getAttribute(\"data-icon\");" \
        "        for (let index = 0; index < waits_for.length; index++) {" \
        "           if (waits_for[index] === attr){" \
        "              return" \
        "           }" \
        "        }" \
        "        await delay();" \
        "     }" \
        " };" \
        " function delay() {" \
        "     return new Promise((resolve, reject) => {" \
        "         setTimeout(() => {" \
        "            resolve("");" \
        "         }, 10);" \
        "     });" \
        " };" \
        f"await waiter(['{'\', \''.join(waits_for)}']);"
        try:
            self.driver.execute_async_script(function_text)
        except Exception as e:
            logger.collect_log(str(e))
            return False
        return True
    
    def waiter(self):
        self.__await_func(["msg-time"])
        self.__await_func(["msg-check", "msg-dblcheck"])
