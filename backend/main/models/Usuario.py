from .. import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre= db.Column(db.String(50), nullable=False)
    contraseña= db.Column(db.String(50), nullable=False)
    rol= db.Column(db.String(50), nullable=False) 
    email= db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return '<Usuario: %r %r >'% (self.nombre, self.contraseña, self.rol, self.email)
    def to_json(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'contraseña': str(self.contraseña),
            'rol':str(self.rol),
            'email':str(self.email),
        }
        return usuario_json
    
    def to_json_short(self):
        usuario_json = {
            'id': self.id,
            'nombre': str(self.nombre),
            'contraseña': str(self.contraseña),
            'email':str(self.email),
        }
        return usuario_json
    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get('id')
        nombre = usuario_json.get('nombre')
        contraseña = usuario_json.get('contraseña')
        rol = usuario_json.get('rol')
        email = usuario_json.get('email')
        return Usuario(id = id,
                        nombre=nombre,
                        contraseña=contraseña,
                        rol=rol,
                        email=email,
                        )