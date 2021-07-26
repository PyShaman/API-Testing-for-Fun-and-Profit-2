import os

from dotenv import load_dotenv


class Config:
    load_dotenv("../.env")
    URL = os.environ["URL"]
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
