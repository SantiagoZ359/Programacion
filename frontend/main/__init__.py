import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager, login_required
from main.routes import routes
#import routes

#login_manager = LoginManager()

def create_app():
    app= Flask(__name__)
    load_dotenv()
    
    app.config['API_URL'] = os.getenv('API_URL')
    
    #login_manager.init_app(app)
    
    #from routes import main
    app.register_blueprint(routes.app)
    #app.register_blueprint(routes.main.main)
    
    return app