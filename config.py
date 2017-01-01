import os
WTF_CSRF_ENABLED=True
SECRET_KEY='-----'
basedir=os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
OAUTH_CREDENTIALS= {
    'facebook': {
        'id': '1273624476010013',
        'secret': 'c0da4260c2755a3c83a87edfe4e4a8e5'
    }
    }
