from itertools import count
from locale import currency
from flask_restful import Resource
from flask import request, jsonify
import jwt


from .. import db
from main.models import PoemaModel
from main.models import UsuarioModel
from main.models import CalificacionModel
from sqlalchemy import func
from datetime import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_mail import Mail
from main.mail.functions import sendMail

#Poemas

#POEMAS = {
#    1:{'nombrepoema': 'Rafaga','Autor':'Lun891'},
#    2:{'nombrepoema': 'La nueva luna','autor':'Juancito1991'},
#}

class Poema(Resource):
    #metodo get
    @jwt_required(optional=True)
    def get(self,id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        
        identidad = get_jwt_identity()
        if identidad:
            return poema.to_json()
        else:
            return poema.to_json_public()
    
    #metodo delete
    @jwt_required()
    def delete(self,id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        #Verificar si se ha ingresado con token
        identidad_usuario = get_jwt_identity()
        
        #Obtener claims de adentro del JWT
        claims = get_jwt()
        #admin o creador pueda borrar el mismo.
        if claims['rol'] == "admin" or poema.usuario_id == identidad_usuario:
            try:
                db.session.delete(poema)
                db.session.commit()
            except Exception as error:
                return 'Formato incorrecto',204
            return '', 201
        else:
            return 'No tienes permiso para realizar esta acción.', 403

    
    
    
    ##metodo put
    #def put(self,id):
    #    poema = db.session.query(PoemaModel).get_or_404(id)
    #    data = request.get_json().items()
    #    for key, valor in data:
    #        setattr(poema,key,valor)
    #    db.session.add(poema)
    #    db.session.commit()
    #    return poema.to_json(), 201


class Poemas(Resource):
    @jwt_required(optional=True)
    def get (self):
        filtros = request.data
        poemas = db.session.query(PoemaModel)
        #definimos en que pag estamos
        pagina = 1
        #cuatos objetos mostramos por pag
        por_pagina = 5
        #definimos el request y los filtros
        filtros = request.get_json().items()
        for key, valor in filtros:
            if key == 'pagina':
                pagina = int(valor)
                #elementos que va a mostrar por pag
            if key == 'por_pagina':
                por_pagina = int(valor)

        identidad_usuario = get_jwt_identity()
        poemas.poetaId = identidad_usuario

        if request.get_json():
            if identidad_usuario:
                poemas = db.session.query(PoemaModel).filter(PoemaModel.usuario_id != identidad_usuario).order_by(PoemaModel.fecha).outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(CalificacionModel.nota)

            else:
                for key, valor in filtros:
                    if key == 'titulo':
                        poemas == poemas.filtro(PoemaModel.titulo.like('%'+valor+'%'))
                #filtro id del autor
                    if key == 'usuario_id':
                        poemas = poemas.filtro(PoemaModel.usuario_id == valor)
                #filtro promedio de calificaciones
                    if key == 'promedio':
                        poemas = poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).having(func.avg(CalificacionModel.nota) == float(valor))
                #filtro fecha gte
                    if key == 'fecha[gt]':
                        poemas == poemas.filtro(PoemaModel.fecha >= datetime.strftime(valor, '%d-%m-%Y'))
                #filtro fecha lte
                    if key == 'fecha[lt]':
                        poemas == poemas.filtro(PoemaModel.fecha <= datetime.strftime(valor, '%d-%m-%Y'))
                #filtro nombre del autor
                    if key == 'nombre_usuario':
                        poemas == poemas.filtro(PoemaModel.usuario.has(UsuarioModel.nombre.like('%'+valor+'%')))

                #Ordentamiento
                if key == "ordenar_por":
                    #Ordenamiento por fechas ascendete
                    if valor == 'fecha_hora':
                        poemas = poemas.order_by(PoemaModel.fecha)
                    #Ordenamiento por fechas descendente
                    if valor == 'fecha_hora[desc]':
                        poemas == poemas.order_by(PoemaModel.fecha.desc())
                    #Ordenamiento por promedio de calificaciones
                    if valor == 'nota':
                        poemas == poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by((PoemaModel.nota))
                    #Ordenamiento por promedio de calificaciones decendente
                    if valor == 'nota[desc]':
                        poemas == poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by((PoemaModel.nota).desc())
                    #Ordenamiento por nombre de autor ascendente
                    if valor == 'nombre_autor':
                        poemas == poemas.outerjoin(PoemaModel.usuario).group_by(UsuarioModel.id).order_by((UsuarioModel.nombre))
                    #Ordenamiento por nombre de autor descendente
                    if valor == 'nombre_autor[desc]':
                        poemas == poemas.outerjoin(PoemaModel.usuario).group_by(UsuarioModel.id).order_by((UsuarioModel.nombre).desc())

        poemas = poemas.paginate(pagina,por_pagina, True, 10)
        return jsonify ({"poemas":[poema.to_json_short() for poema in poemas.items],
        "total": poemas.total, "paginas": poemas.pages, "pagina": pagina})

    @jwt_required()
    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        #se obtiene el id del usuario autenticado
        identidad_usuario = get_jwt_identity()
        #se asocia el poema con el usuario
        poema.usuario_id = identidad_usuario
        
        usuario = db.session.query(UsuarioModel).get(identidad_usuario)

        claims = get_jwt
        if len(usuario.poemas) == 0 or len(usuario.calificaciones)/len(usuario.poemas) > 5 and claims['rol'] != "admin":

            try:
                db.session.add(poema)
                db.session.commit()
                send = sendMail([calificacion.poema.usuario.email],"Tu poema ha sido calificado",'calificado', usuario1 = usuario, usuario = Calificacion.poema.usuario, poema = Calificacion.poema)
            except Exception as error:
                return 'Formato incorrecto', 400
            return poema.to_json(), 201
        else:
            return 'Antes debes calificar 5 poemas para subir uno nuevo. (Los administradores no pueden subir poemas)', 404