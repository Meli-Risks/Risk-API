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

# JWT access token expiration time (30 minutes)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

# JWT refresh token expiration time (24 hours)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=24)

# Enable JWT token blacklist
JWT_BLACKLIST_ENABLED = True

# Swagger config
SWAGGER = {
    'title': 'API Documentation',
    'uiversion': 3,
    'openapi': '3.0.3',
    'url_prefix': '/api/v1',
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/static/oas.json'
        }
    ]
}