import asyncio
import time
import os

from messageSender.sender import Sender, AsyncSender
from messageSender.WhatsAppSender import constants
from utils import logger, config

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WASender(Sender, AsyncSender):
    async def await_for_element(self, selector, count) -> bool:
        save_wait = config.TIMEOUT
        while len(self.driver.execute_script(f'return document.querySelectorAll(\'{selector}\')')) < count and save_wait > 0:
            await asyncio.sleep(config.TIMEDIFF)
            save_wait = save_wait - 1

        return save_wait > 0

    def wait_for_element(self, selector, count) -> bool:
        save_wait = config.TIMEOUT
        while self.driver.execute_script(f'return document.querySelectorAll(\'{selector}\').length') < count and save_wait > 0:
            time.sleep(config.TIMEDIFF)
            save_wait = save_wait - 1

        return save_wait > 0

    def __enter__(self):
        self.driver = self.driver_class(options=self.options)
        self.driver.get(constants.WA_URL)

        if not self.wait_for_element("#side", 1):
            raise ValueError

        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.ESCAPE)
        self.current = None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.sleep(1)
        self.driver.quit()

    def __init__(self, options: webdriver.ChromeOptions = webdriver.ChromeOptions(), driver_class = webdriver.Chrome, profile_path = os.path.join(os.getcwd(), "profile")):
        if not os.path.exists(profile_path):
            os.mkdir(profile_path)

        self.driver_class = driver_class

        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
        options.add_argument(f'user-data-dir={os.path.abspath(profile_path)}')
        options.add_argument('--profile-directory=Profile1')
        options.add_argument('--profiling-flush=n')
        options.add_argument('--enable-aggressive-domstorage-flushing')

        self.options = options
        self.current = None

        super().__init__()


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

    def __set_text(self):
        text = self.template

        for replace, to in self.variables.items():
            text = text.replace(replace, to)

        return text

    def send_text(self, to: str) -> bool:
        self.__go_to_user(to)

        if not self.wait_for_element("footer button", 3):
            logger.collect_log(f"text is not sended for {to}")
            return False

        self.paste_text(self.__set_text())
        self.send()

        return self.waiter()

    async def a_send_text(self, to) -> bool:
        self.__go_to_user(to)

        if await self.await_for_element("footer button", 3):
            logger.collect_log(f"text is not sended for {to}")
            return False

        self.paste_text(self.__set_text())
        self.send()

        self.waiter()
        return True

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
            'let items = document.querySelectorAll("div:has(+input) div[role=\'button\']:has(> span > svg)");' 
            'console.log(items);'
            'items[1].click()'
        )

        timeout = self.waiter()
        if not timeout:
            logger.collect_log(f"image {image_path} not sended for {to}, timeout")
        os.remove(image_path)
        return timeout

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

    @staticmethod
    def __wait_func_text(waits_for: list[str]) -> str:
        return "async function waiter(waits_for) {" \
            "console.log(waits_for);" \
            "let save_freeze = 0;" \
            "while (save_freeze < 10000000) {" \
                "save_freeze++;" \
                "let l = document.querySelectorAll(\"div[role='application'] div[role='row']\");" \
                "let el = l[l.length - 1].querySelector(\"span+div>span[aria-hidden='false']\");" \
                "if (el === null) {await delay(); continue}" \
                "let attr = el.getAttribute(\"data-icon\");" \
                "console.log(attr);" \
                "await delay();" \
                "for (let index = 0; index < waits_for.length; index++) {" \
                    "console.log(waits_for[index] === attr);" \
                    "if (waits_for[index] === attr){" \
                        "return true" \
                    "}" \
                "}" \
            "}; return false;" \
        "};" \
        "function delay() {" \
            "return new Promise((resolve, reject) => {" \
                "setTimeout(() => {" \
                    "resolve("");" \
                "}, 10);" \
            "});" \
        "};" \
        f"let out = await waiter(['{'\', \''.join(waits_for)}']); return out;"

    def __waiting(self, waits_for: list[str]):
        is_found = False
        try:
           is_found = self.driver.execute_script(self.__wait_func_text(waits_for))
        except Exception as e:
           logger.collect_log(f"Exception: {e}", "exception")

        return is_found

    def waiter(self):
        wait = self.__waiting(["msg-time"]) and self.__waiting(["msg-check", "msg-dblcheck"])
        time.sleep(0.05)
        return wait
