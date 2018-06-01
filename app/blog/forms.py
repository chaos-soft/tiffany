from wtforms import FileField, SubmitField, StringField, HiddenField, \
    validators
from common.forms import Form


class ArticleForm(Form):
    title = StringField('Заголовок', [validators.required()])
    images_ids = HiddenField('images_ids')
    submit = SubmitField('Сохранить')


class ImageForm(Form):
    image = FileField('path', render_kw={'multiple': 'multiple'})
    submit = SubmitField('Загрузить')


class ImageDeleteForm(Form):
    images_ids = HiddenField('images_ids', [validators.required()])
    submit = SubmitField('Удалить', render_kw={'disabled': 'disabled'})


class ArticleDeleteForm(Form):
    articles_ids = HiddenField('articles_ids', [validators.required()])
    submit = SubmitField('Удалить', render_kw={'disabled': 'disabled'})
