import json
import os

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

with open(os.path.join(os.getcwd(), "configs", "endpoints.json"), "r") as config_file:
    ENDPOINTS = json.load(config_file)
