from messageSender import sender

from messageSender.WhatsAppSender import wasender
from messageSender.WhatsAppBusinessApiSender import waba_sender

WORKING_SENDERS: dict[str, type[sender.Sender]] = {
    'WhatsApp пользователя': wasender.WASender,
    'WhatsApp Business': waba_sender.WhatsAppApiSender
}
