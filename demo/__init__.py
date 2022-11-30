from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def create_app():
    app=Flask(__name__,template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/school'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.app_context().push()
    from . models import User
    from . views import views
    app.register_blueprint(views, url_prefix='/')
    db.init_app(app)
    return app
