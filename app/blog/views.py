from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from common import db
from sqlalchemy.orm import selectinload

from .models import Article, Image, ArticleImage
from .forms import ImageForm, ArticleForm, ImageDeleteForm, ArticleDeleteForm

bp = Blueprint('blog', __name__)


@bp.route('/', methods=('GET',))
def index():
    articles = Article.query.options(selectinload('images')).all()
    return render_template('blog/index.html', articles=articles)


@bp.route('/articles/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    article = Article.query.get(id)
    form = ArticleForm(request.form, article)

    if request.method == 'POST' and form.validate():
        images_ids = set(map(int, filter(bool, form.images_ids.data.split(','))))
        form.populate_obj(article)
        articles_images = []
        ArticleImage.query.filter(ArticleImage.article_id == article.id). \
            delete()

        for image_id in images_ids:
            articles_images.append(ArticleImage(article_id=article.id,
                                                image_id=image_id))

        if articles_images:
            db.session.add_all(articles_images)

        db.session.commit()
        return redirect(url_for('.edit', id=id))

    images = Image.query
    images_ids = [image.id for image in article.images]
    form.images_ids.data = ','.join(map(str, images_ids))
    return render_template('form.html',
                           form=form,
                           form_action=url_for('.edit', id=id),
                           title='Редактировать статью',
                           form_include='blog/images_mixin.html',
                           images=images,
                           images_ids=images_ids,
                           header_include='blog/header_mixin.html')


@bp.route('/images/upload', methods=('GET', 'POST'))
def upload():
    form = ImageForm(request.form)

    if request.method == 'POST' and form.validate() and request.files:
        images = []

        for v in request.files.getlist('image'):
            filename = secure_filename(v.filename)
            images.append(Image(image='/'.join((Image.UPLOAD_TO, filename))))
            v.save(images[-1].get_path())

        if images:
            db.session.add_all(images)
            db.session.commit()

        return redirect(url_for('.images'))

    return render_template('form.html',
                           form=form,
                           form_action=url_for('.upload'),
                           title='Загрузить картинки',
                           header_include='blog/header_mixin.html')


@bp.route('/images', methods=('GET', 'POST'))
def images():
    form = ImageDeleteForm(request.form)

    if request.method == 'POST' and form.validate():
        images_ids = set(map(int, filter(bool, form.images_ids.data.split(','))))
        images = Image.query.filter(Image.id.in_(images_ids))

        for image in images:
            image.delete_file()

        ArticleImage.query.filter(ArticleImage.image_id.in_(images_ids)). \
            delete(synchronize_session=False)
        images.delete(synchronize_session=False)
        db.session.commit()
        return redirect(url_for('.images'))

    return render_template('form.html',
                           form=form,
                           form_action=url_for('.images'),
                           title='Картинки',
                           form_include='blog/images_mixin.html',
                           menu_include='blog/images_menu_mixin.html',
                           header_include='blog/header_mixin.html',
                           images=Image.query,
                           form_name='blog')
