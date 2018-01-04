from os import path


class Configuration(object):
    # Statement for enabling the development environment
    DEBUG = True
    DEVELOPMENT = True

    DATABASE_NAME = "ebooks.db"

    PUBLIC_IP = "0.0.0.0"
    BASE_DIR = path.abspath(path.dirname(__file__))

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    # Disable Flask-Restful 404 Help message showing other endpoints
    # closely matching the one tested
    ERROR_404_HELP = False

    # Secret key for signing cookies
    SECRET_KEY = "secret"