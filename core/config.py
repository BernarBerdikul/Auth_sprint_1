import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

PWD_SECRET_KEY: str = "secret_key"
# ключ для JWS токена, не использовать на проде
JWT_SECRET_KEY: str = "super_secret"
JWT_BLACKLIST_ENABLED: bool = True
JWT_COOKIE_SECURE: bool = False
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
TESTING: bool = os.getenv("TESTING") == "True"

# Корень проекта
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
