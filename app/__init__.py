import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
#上面的'login'值是登入檢視函式（endpoint）名，
# 換句話說該名稱可用於url_for()函式的引數並返回對應的 URL。

#最後，我在底部匯入了一個名為models的模組，這個模組將會用來定義資料庫結構。
#為了讓這些錯誤處理程式在 Flask 中註冊，我需要在應用例項建立後匯入新的app/errors.py模組。
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], 
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
        #啟用另一個基於檔案型別RotatingFileHandler的日誌記錄
        # 需要以和電子郵件日誌記錄器類似的方式將其附加到應用的 logger 物件中。
        """
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                        backupCount=10)
        #RotatingFileHandler 類非常棒，
        # 因為它可以切割和清理日誌檔案，
        # 以確保日誌檔案在應用執行很長時間時不會變得太大。 
        # 本處，我將日誌檔案的大小限制為 10KB，
        # 並只保留最後的十個日誌檔案作為備份。
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        #logging.Formatter 類為日誌訊息提供自定義格式。 
        # 由於這些訊息正在寫入到一個檔案，
        # 我希望它們可以儲存儘可能多的資訊。 
        # 所以我使用的格式包括時間戳、日誌記錄級別、
        # 訊息以及日誌來源的原始碼檔案和行號。
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        """

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
    return app

@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return 'zh_hant_TW'


from app import models  # <-- remove errors from this import!