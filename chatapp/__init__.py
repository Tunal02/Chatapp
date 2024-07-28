from flask import Flask
from .events import sio
from .extensions import db
from flask_bcrypt import Bcrypt
from flask_login import *
login=LoginManager()
bcrypt=Bcrypt()
def create_app():
    app=Flask(__name__)
    app.config["DEBUG"]=True
    app.config["SECRET_KEY"]="74fc9963af4ffb85db3b6fd6fc6e67889106a8493cf5b27e9add3c3f12f47818"
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.site3'
    
    db.init_app(app)
    from .routes import main
    app.register_blueprint(main)
    sio.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    with app.app_context():
        db.create_all()

    return app
