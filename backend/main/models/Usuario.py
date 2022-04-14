import email
from .. import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre= db.Column(db.String(50), nullable=False)
    contraseña= db.Column(db.String(50), nullable=False)
    rol= db.Column(db.String(50), nullable=False) 
    email= db.Column(db.String(50), nullable=False)