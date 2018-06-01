from app import app
from wtforms.csrf.session import SessionCSRF
from wtforms import form
from flask import session


class Form(form.Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = app.config['SECRET_KEY']

        @property
        def csrf_context(self):
            return session
