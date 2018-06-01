import os

DEBUG = True
DATABASE_URI = 'mysql+pymysql://root:root@localhost/tiffany?charset=utf8'
SECRET_KEY = b'U;kOI/75G5MYuu@S(K[XFnStgEFG>.o8++{:eNrme81@qGEO(9_JVvTc,wmVbm|'
ENV = 'development'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
