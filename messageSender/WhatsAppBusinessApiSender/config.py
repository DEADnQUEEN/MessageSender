import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TOKEN = os.getenv("API_KEY")

TEMPLATE_ARGS = {
    "namespace": os.getenv("NAMESPACE"),
    "template": os.getenv("TEMPLATE_NAME"),
    "language": {
        "policy": "deterministic",
        "code": "ru"
    },
}
with open(os.path.join(os.getcwd(), "configs", "endpoints.json"), "r") as config_file:
    ENDPOINTS = json.load(config_file)
