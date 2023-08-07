""""Module for extract environments variables for use in project."""


import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_URL_LOCAL = os.environ.get("DATABASE_URL_LOCAL")
DATABASE_URL_REMOTE = os.environ.get("DATABASE_URL_REMOTE")
#DATABASE_URL = DATABASE_URL_LOCAL
DATABASE_URL = DATABASE_URL_REMOTE
# DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
