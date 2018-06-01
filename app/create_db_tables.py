from app import app
import blog.models
from common import db, models

models.Base.metadata.create_all(bind=db.engine)
