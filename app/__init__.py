import os
import logging
from logging.handlers import RotatingFileHandler


from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash


from .settings import Settings, users


app = Flask(__name__)
app.config.from_object(Settings)
auth = HTTPBasicAuth()


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/rpi-monitor.log', maxBytes=10240, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('RPi monitor startup')


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


from app import routes, models, commands, sidebar
