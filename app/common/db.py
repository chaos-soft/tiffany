from app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(app.config['DATABASE_URI'], echo=app.config['DEBUG'])
session = scoped_session(sessionmaker(bind=engine))
