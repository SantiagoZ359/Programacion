from email.policy import default
from sqlite3 import Timestamp
from .. import db

class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    usuario_id = db.Column(db.Integer())
    cuerpo =db.Column(db.String(500), nullable=False)
    fecha =db.Column(default=Timestamp.now(), nullable=False)
    def __repr__(self):
        return '<Poema: %r %r >' % (self.titulo, self.usuario_id, self.cuerpo, self.fecha)
    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'usuario_id': int(self.usuario_id),
            'cuerpo': str(self.cuerpo),
            'fecha': str(self.fecha),
        }
        return poema_json

    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
        }
        return poema_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(poema_json):
        id = poema_json.get('id')
        usuario_id = poema_json.get('usuario_id')
        titulo = poema_json.get('titulo')
        cuerpo = poema_json.get('cuerpo')
        fecha = poema_json.get('fecha')
        return Poema(id=id,
                    titulo=titulo,
                    usuario_id=usuario_id,
                    cuerpo=cuerpo,
                    fecha=fecha
                    )
