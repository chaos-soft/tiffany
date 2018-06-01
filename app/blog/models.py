import os

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from common.models import Base
from common.imagemagick import create_thumbnail, delete_thumbnail
from app import app
from flask import url_for


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

    images = relationship('Image',
                          secondary='articles_images',
                          back_populates='articles',
                          lazy='select')

    def __str__(self):
        return self.title

    def get_image(self):
        return url_for('static', filename=self.images[0].image) if self.images else None


class Image(Base):
    __tablename__ = 'images'

    UPLOAD_TO = 'blog'

    id = Column(Integer, primary_key=True)
    image = Column(String(300), nullable=False)

    articles = relationship('Article',
                            secondary='articles_images',
                            back_populates='images',
                            lazy='select')

    def __str__(self):
        return self.image.split('/')[-1]

    def get_path(self):
        return os.path.join(app.config['STATIC_FOLDER'], self.image)

    def delete_file(self):
        delete_thumbnail(self, size=r'20000x320\>')

        if os.path.isfile(self.get_path()):
            os.remove(self.get_path())

    def get_thumbnail(self):
        return create_thumbnail(self, size=r'20000x320\>')


class ArticleImage(Base):
    __tablename__ = 'articles_images'

    article_id = Column(Integer, ForeignKey('articles.id'), primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
