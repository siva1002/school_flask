from flask import Flask,render_template,request
from flask_admin import Admin
from .extension import db
from . views import views
from flask_migrate import Migrate
def create_app():
    app=Flask(__name__,template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/school'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['DEBUG']=True
    admin=Admin(app,name='Controll Panel')
    app.app_context().push()
    app.register_blueprint(views, url_prefix='/')
    db.init_app(app)
    Migrate(app,db)
    return app
