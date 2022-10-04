import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
#SQLALCHEMY_DATABASE_URI = 'postgresql://buokem:buokem@localhost:5432/fyyur'
SQLALCHEMY_DATABASE_URI = 'postgres://gnlssslhwufyzz:8d9102e1760799256235f693a971ea5b833764878fb9fd898dd7d615ae7a1ffc@ec2-3-92-98-129.compute-1.amazonaws.com:5432/d3kgcih8d3tlee'
