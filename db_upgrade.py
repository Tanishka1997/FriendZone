from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from migrate.versioning import api
api.upgade(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO)
v=api.db_version(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO)
print("VERSION: "+str(v))
