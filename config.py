import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 40 # 每页显示 ip 数目
    USERS_PER_PAGE = 10 # 每页显示 user 数目

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
