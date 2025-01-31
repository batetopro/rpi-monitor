import os


from werkzeug.security import generate_password_hash



basedir = os.path.abspath(os.path.dirname(__file__))


users = {
    'admin': generate_password_hash('changeme'),
}


class Settings(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    