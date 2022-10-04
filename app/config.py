import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
#SQLALCHEMY_DATABASE_URI = 'postgresql://buokem:buokem@localhost:5432/fyyur'
SQLALCHEMY_DATABASE_URI = 'postgres://apajblqiprtuxn:bcff78238e24e158b26aa866f32d549c1295a96d23b2c2ab594fd42b18c86270@ec2-3-92-98-129.compute-1.amazonaws.com:5432/df6ein33quthou'
