import os
from datetime import timedelta

# Database connection string
SQLALCHEMY_DATABASE_URI = os.environ.get('CONNECTION_STRING')

# Enable or disable debugging mode
DEBUG = True

# Enable SQLAlchemy echoing
SQLALCHEMY_ECHO = False

# Secret key for JWT
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# Enable JWT protection against CSRF attacks using cookies
JWT_COOKIE_CSRF_PROTECT = True

# Enable JWT CSRF check for form submissions
JWT_CSRF_CHECK_FORM = True

# JWT access token expiration time (2 minutes)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)

# Enable JWT token blacklist
JWT_BLACKLIST_ENABLED = True
