import os
from dotenv import load_dotenv

load_dotenv(".env")

class Settings:
    def __init__(self):
        self.API_VERSION = os.getenv("API_VERSION")
        self.POD_NAME = os.getenv("POD_NAME")
        self.PORT = os.getenv("PORT")
        self.OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

settings = Settings()
