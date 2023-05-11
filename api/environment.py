import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    DATE_FORMAT = os.environ['DATE_FORMAT']
    SECRET_KEY  = os.environ['SECRET_KEY']
    TOKEN_EXPIRATION = int(os.environ['TOKEN_EXPIRATION_IN_DAYS'])