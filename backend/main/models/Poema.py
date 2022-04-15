from datetime import datetime
from .. import db

current_date = datetime.today().strftime('%A, %B %D, %Y %H:%M:%S')

class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    cuerpo =db.Column(db.String(500), nullable=False)
    fecha =db.Column(db.Integer(current_date), nullable=False)
    def __repr__(self):
        return '<Poema: %r %r %r %r >' % (self.titulo, self.usuario_id, self.cuerpo, self.fecha)
    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'autor_id': int(self.usuario_id),
            'cuerpo': str(self.cuerpo),
            'fecha': int(self.fecha),
        }
        return poema_json

    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'autor_id': int(self.usuario_id),
            'cuerpo':str(self.cuerpo),
            'fecha':int(self.fecha)
        }
        return poema_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(poema_json):
        id = poema_json.get('id')
        autor = poema_json.get('autor_id')
        titulo = poema_json.get('titulo')
        cuerpo = poema_json.get('cuerpo')
        fecha = poema_json.get('fecha')
        return Poema(id=id,
                    titulo=titulo,
                    autor=autor,
                    cuerpo=cuerpo,
                    fecha=fecha,
                    )
