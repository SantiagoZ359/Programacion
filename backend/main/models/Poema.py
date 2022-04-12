from .. import db

class Poema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<Poema: %r %r >' % (self.titulo, self.autor)
    def to_json(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.titulo),
            'autor': str(self.autor),

        }
        return poema_json

    def to_json_short(self):
        poema_json = {
            'id': self.id,
            'titulo': str(self.autor),

        }
        return poema_json
    @staticmethod
    #Convertir JSON a objeto
    def from_json(poema_json):
        id = poema_json.get('id')
        autor = poema_json.get('titulo')
        titulo = poema_json.get('autor')
        return Poema(id=id,
                    titulo=titulo,
                    autor=autor,
                    )
