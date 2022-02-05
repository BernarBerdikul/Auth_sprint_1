DEFAULT_ROLE_FOR_ALL_USERS: str = "simple_user"
ROLE_FOR_ADMIN: str = "admin"

USERNAME_MIN_LENGTH: int = 5
USERNAME_MAX_LENGTH: int = 35
REGEX_FOR_FIRST_SYMBOL: str = r"^[A-Z]"
REGEX_FOR_LOGIN: str = r"^[a-zA-Z0-9_]+$"


PASSWORD_MIN_LENGTH: int = 8
PASSWORD_MAX_LENGTH: int = 50
REGEX_ALPHABET_IN_PASSWORD: str = r"^[a-zA-Z0-9_!#?.]+$"
REGEX_PASSWORD_INT_SYMBOL: str = r"[0-9]+"
REGEX_UPPER_LATTER_IN_PASSWORD: str = r"[A-Z]+"
REGEX_LOWER_LATTER_IN_PASSWORD: str = r"[a-z]+"