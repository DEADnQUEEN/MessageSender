import requests
import json

from messageSender import sender
from messageSender.WhatsAppBusinessApiSender import config

from utils import logger


def send_request(endpoint: str, method: str, **kwargs):
    if endpoint not in config.ENDPOINTS.keys():
        raise KeyError

    response = requests.request(
        method=method,
        url=f"{config.BASE_URL}{config.ENDPOINTS[endpoint]}?token={config.TOKEN}",
        headers={
            'Content-Type': 'application/json',
        },
        **kwargs
    )

    response.raise_for_status()
    return response.json()


class WhatsAppApiSender(sender.Sender):
    def send_text(self, to) -> bool:
        data = {**self.default_data}
        data['params'][0]['parameters'] = [
            {
                "type": "text",
                'text': value
            }
            for value in self.values
        ]
        data['phone'] = f"{to}"
        try:
            send_request(
                endpoint='text',
                method="post",
                data=json.dumps(
                    data
                )
            )
            return True
        except Exception as e:
            logger.collect_log(str(e), "wa_api_send")
            return False

    def send_image(self, to, image_path) -> bool:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
