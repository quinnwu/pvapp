import os, sys
from datetime import datetime

SECRET_KEY = "something secret"

MAIL_SERVER = ""
MAIL_PORT = 465
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
SQLALCHEMY = 'mysql://nkav:theorder@localhost/pvapp'

HOME_FOLDER = os.path.dirname(__file__) 
UPLOAD_FOLDER = os.path.join(HOME_FOLDER, 'static/submissions') 
STATIC_FOLDER = os.path.join(HOME_FOLDER, 'static/img') 

# admin settings
ADMIN_EMAIL = "pennvention@gmail.com"
ADMIN_PASS = "wthPV13-14"

ROUND_1_START_DATE = datetime(2016,01,01)
ROUND_1_END_DATE = datetime(2016,02,15, 5, 00, 00)
COMPETITION_CYCLE = 2016
