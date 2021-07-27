import os

from dotenv import load_dotenv


class Config:
    load_dotenv("../.env")
    URL = os.environ.get("URL")
    USR = os.environ.get("USR")
    PWD = os.environ.get("PWD")
