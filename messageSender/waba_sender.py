from messageSender import sender

class WhatsAppApiSender(sender.Sender):
    def send_text(self, to, text) -> bool:
        raise NotImplementedError()

    def send_image(self, to, image_path) -> bool:
        raise NotImplementedError()
