from flask_restful import Resource
from flask import request, jsonify
from main.models import UsuarioModel
from .. import db

#Usuarios

USUARIOS = {
    1:{'nombre-usuario': 'Carlos','nickname-usuario':'Lun891'},
    2:{'nombre-usuario': 'Juan','nickusuario':'Juancito1991'},
}

class Usuario(Resource):
    def get(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_jason()
    def delete(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class Usuarios(Resource):
    def get(self):
        usuarios = db.session.query(UsuarioModel).all()
        return jsonify([UsuarioModel.to_json_short(self) for usuario in usuarios])

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201