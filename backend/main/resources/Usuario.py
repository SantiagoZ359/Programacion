import resource
from flask_restful import Resource
from flask import request

#Usuarios

USUARIOS = {
    1:{'nombre-usuario': 'Carlos','nickname-usuario':'Lun891'},
    2:{'nombre-usuario': 'Juan','nickusuario':'Juancito1991'},
}

class Usuario(Resource):
    def get(self,id):
        if int(id) in USUARIOS:
            return USUARIOS[int(id)]
        return '',404
    def delete(self,id):
        if int(id) in USUARIOS:
            del USUARIOS[int(id)]
            return'',204
        return'',404

class Usuarios(Resource):
    def get (self):
        return USUARIOS
    def post(self):
        Poemas = request.get_json()
        id = int(max(USUARIOS.keys())) + 1
        USUARIOS[id] = Usuario
        return USUARIOS[id], 201
