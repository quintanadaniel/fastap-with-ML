import os

from datadog import initialize, statsd
from dotenv import load_dotenv


load_dotenv()


class DatadogClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.app_key = os.getenv("APP_KEY")

    def client_initialize(self):
        options = {"api_key": self.api_key, "app_key": self.app_key}
        return initialize(**options)

    def send_metrics_incremental(self, name: str):
        return statsd.increment(name, 1)
