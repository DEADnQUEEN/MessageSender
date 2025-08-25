import requests
import json

from messageSender import sender
from messageSender.WhatsAppBusinessApiSender import config

from utils import logger


def get_endpoint(endpoint: str):
    if endpoint not in config.ENDPOINTS.keys():
        raise KeyError

    return f"{config.BASE_URL}{config.ENDPOINTS[endpoint]}?token={config.TOKEN}"

class WhatsAppApiSender(sender.Sender):
    @staticmethod
    def send_get_request(endpoint):
        url = get_endpoint(endpoint)

        response = requests.get(
            url=url,
            headers={
                'Content-Type': 'application/json',
            }
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.collect_log(str(e), "http_error")
            raise e
        return response.json()

    @staticmethod
    def send_text_template(to):
        response =requests.post(
            url=get_endpoint(endpoint=config.ENDPOINTS['template']),
            data=json.dumps(
                {

                }
            )
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.collect_log(str(e), "http_error")
            raise e

    def send_text(self, to) -> bool:
        response =requests.post(
            url = get_endpoint(endpoint=config.ENDPOINTS['text']),
            data=json.dumps(
                {

                }
            )
        )
        try:
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            logger.collect_log(str(e), "http_error")
            return False

    def send_image(self, to, image_path) -> bool:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
