from .. import db

class Calificacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nota= db.Column(db.String(50), nullable=False)
    comentario= db.Column(db.String(50), nullable=True)
    usuario_id= db.Column(db.Integer, primary_key=True) 
    poema_id= db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return '<Calificacion: %r %r %r %r >'% (self.nota, self.comentario, self.usuario_id, self.poema_id)
    def to_json(self):
        calificacion_json = {
            'id': self.id,
            'nota': str(self.nota),
            'comentario': str(self.comentario),
            'usuario':str(self.usuario_id),
            'poema':str(self.poema_id),
        }
        return calificacion_json
    
    def to_json_short(self):
        calificacion_json = {
            'id': self.id,
            'nota': str(self.nota),
            'comentario': str(self.comentario),
            'usuario': str(self.usuario_id),
            'poema':str(self.poema_id),
        }
        return calificacion_json
    @staticmethod
    def from_json(calificacion_json):
        id = calificacion_json.get('id')
        nota = calificacion_json.get('nota')
        comentario = calificacion_json.get('comentario')
        usuario = calificacion_json.get('usuario')
        poema = calificacion_json.get('poema')
        return Calificacion(id = id,
                        nota=nota,
                        comentario=comentario,
                        usuario = usuario,
                        poema= poema,
                        )