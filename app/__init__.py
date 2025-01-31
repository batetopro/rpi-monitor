from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash


from .settings import Settings, users


app = Flask(__name__)
app.config.from_object(Settings)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


app = Flask(__name__)


from app import routes, models, commands
