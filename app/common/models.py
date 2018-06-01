from sqlalchemy.ext.declarative import declarative_base

from . import db

Base = declarative_base()
Base.query = db.session.query_property()
