import requests
import json
from messageSender import sender
from messageSender.WhatsAppBusinessApiSender import config


class WhatsAppApiSender(sender.Sender):
    @staticmethod
    def __send_post_request(endpoint: str, **data):
        data['token'] = config.API_KEY
        return requests.post(
            url=f"{config.BASE_URL}{endpoint}",
            data=json.dumps(data),
        )

    def send_text(self, to, text: str) -> bool:
        response = self.__send_post_request(
            endpoint=config.ENDPOINTS['text'],
            body=text,
            phone=to
        )
        response.raise_for_status()
        return True

    def send_image(self, to, image_path) -> bool:
        raise NotImplementedError()
