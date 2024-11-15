import os

# Use the DATABASE_URL from Heroku environment variable if it exists;
# otherwise, default to the local database URL.
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:messi10@localhost:5432/budget')
SQLALCHEMY_TRACK_MODIFICATIONS = False
