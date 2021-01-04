import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
"""
不要將 .env 檔案加入到原始碼版本控制中，這非常重要。否則，
一旦你的密碼和其他重要資訊上傳到遠端程式碼庫中後，你就會後悔莫及。
"""
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['zopq4565@gmail.com']
    POSTS_PER_PAGE = 25

    LANGUAGES = ['en', 'zh_hant_TW']

    MS_TRANSLATOR_KEY = '7195845ad8994c6fb33078d4da322c60'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')


