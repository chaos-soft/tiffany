from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from common import db
import blog.views

app.register_blueprint(blog.views.bp)


@app.teardown_appcontext
def remove_session(exception=None):
    db.session.remove()
