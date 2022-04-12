import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import main.resources as resources

db = SQLAlchemy()
api = Api()

def create_app():
    app= Flask(__name__)
    load_dotenv()

    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)


    api.add_resource(resources.CalificacionesResource, '/calificaciones')
    api.add_resource(resources.CalificacionResource, '/calificacion/<id>')
    api.add_resource(resources.PoemasResource, '/poemas')
    api.add_resource(resources.PoemaResource, '/poema/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.init_app(app)
    return app