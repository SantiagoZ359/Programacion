from flask_restful import Resource
from flask import request, jsonify
from main.models import UsuarioModel, CalificacionModel, PoemaModel
from .. import db
from sqlalchemy import func

#Usuarios

#USUARIOS = {
#    1:{'nombre-usuario': 'Carlos','nickname-usuario':'Lun891'},
#    2:{'nombre-usuario': 'Juan','nickusuario':'Juancito1991'},
#}

class Usuario(Resource):
    def get(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        return usuario.to_json()
    def delete(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '',204
    def put(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key,value in data:
            setattr(usuario,key,valor)
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201


class Usuarios(Resource):
    def get(self):
        pagina = 1
        por_pagina = 10
        usuarios = db.session.query(UsuarioModel)
        if request.get_json():
            filtros = request.get_json().items()
            for key, valor in filtros:
                #paginacion
                if key == "pagina":
                    pagina = int(valor)
                if key == "por_pagina":
                    por_pagina = int(valor)
                
                #filtro nombre
                if key == 'nombre':
                    usuarios = usuarios.filtro(UsuarioModel.nombre.like('%'+valor+'%'))
                
                #ordenamientos
                if key == "ordenar_por":
                    #Por nombre ascendente
                    if key == 'nombre':
                        usuarios = usuarios.order_by(UsuarioModel.nombre.like('%'+valor+'%'))
                    #Por nombre descendente
                    if valor == 'npoemas[desc]':
                        usuarios = usuarios.order_by(func.count(UsuarioModel.id).desc())
                    #Por poemas ascendente
                    if valor == 'num_poemas':
                        print("Dentro")
                        usuarios = usuarios.outerjoin(UsuarioModel.calificaciones).group_by(func.count(UsuarioModel.id))

        users = usuarios.paginacion(pagina, por_pagina, True,18)
        return jsonify({'usuarios': [usuario.to_json_short() for usuario in usuarios.items],
                    'total':usuarios.total,
                    'paginas':usuarios.pages,
                    'pagina': pagina
                    })

    def post(self):
        usuario = UsuarioModel.from_json(request.get_json())
        db.session.add(usuario)
        db.session.commit()
        return usuario.to_json(), 201