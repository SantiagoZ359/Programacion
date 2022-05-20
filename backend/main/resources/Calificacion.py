from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CalificacionModel
from main.models import UsuarioModel
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import admin_required

#Calificaciones

#CALIFICACIONES = {
#    1:{'calificacion': '8','Autor':'Lun891'},
#    2:{'calificacion': '10','Autor':'Juancito1991'},
#}

class Calificacion(Resource):
    def get(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()
    
    @jwt_required()
    def delete(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        identidad_usuario = get_jwt_identity()
        calificacion.calificacionId = identidad_usuario
        claims = get_jwt()
        if calificacion.usuario_id == identidad_usuario or claims['rol'] == "admin":
            try:
                db.session.delete(calificacion)
                db.session.commit()
            except Exception as error:
                return 'Formato Invalido', 204
            return 'Eliminado', 201
        else:
            return 'No tienes permisos para realizar esta accion.', 403
    
    @jwt_required()
    def put(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        identidad_usuario = get_jwt_identity()
        calificacion.calificacionId = identidad_usuario
        if calificacion.usuario_id == identidad_usuario:
            try:
                data = request.get_json().items()
                for key, valor in data:
                    setattr(calificacion,key,valor)
                db.session.add(calificacion)
                db.session.commit()
            except Exception as error:
                return 'Formato Invalido', 204
            return calificacion.to_json(), 201
        else:
            return 'No tienes permiso para realizar esta accion.', 403

class Calificaciones(Resource):
    def get (self):
        calificaciones = db.session.query(CalificacionModel).all()
        return jsonify ([calificacion.to_json_short() for calificacion in calificaciones])

    @jwt_required()
    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        identidad_usuario = get_jwt_identity
        calificacion.calificacionId = identidad_usuario
        claims = get_jwt()

        if identidad_usuario and claims["rol"] != "admin":
            try:
                db.session.add(calificacion)
                db.session.commit()
            except Exception as error:
                return 'Formato incorrecto', 400
            return calificacion.to_json(), 201
        else:
            return 'No dispones de permisos para realizar esta accion.!', 403