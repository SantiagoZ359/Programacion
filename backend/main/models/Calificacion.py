from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nota= db.Column(db.Integer(),nullable=False)
    comentario= db.Column(db.String(50), nullable=True)
    usuario_id= db.Column(db.Integer()) 
    poema_id= db.Column(db.Integer())
    
    def __repr__(self):
        return '<Calificacion: %r %r >'% (self.nota, self.comentario, self.usuario_id, self.poema_id)
    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'nota': str(self.nota),
            'comentario': str(self.comentario),
            'usuario_id':int(self.usuario_id),
            'poema_id':int(self.poema_id),
        }
        return calificacion_json
    
    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'nota': str(self.nota),
        }
        return calificacion_json
    @staticmethod
    def from_json(calificacion_json):
        id = calificacion_json.get('id')
        nota = calificacion_json.get('nota')
        comentario = calificacion_json.get('comentario')
        usuario_id = calificacion_json.get('usuario_id')
        poema_id = calificacion_json.get('poema_id')
        return Calificacion(id = id,
                        nota=nota,
                        comentario=comentario,
                        usuario_id = usuario_id,
                        poema_id= poema_id,
                        )