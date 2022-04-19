from flask_restful import Resource
from flask import request, jsonify
from main.models import CalificacionModel
from .. import db

#Calificaciones

#CALIFICACIONES = {
#    1:{'calificacion': '8','Autor':'Lun891'},
#    2:{'calificacion': '10','Autor':'Juancito1991'},
#}

class Calificacion(Resource):
    def get(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        return calificacion.to_json()
    def delete(self,id):
        calificacion = db.session.query(CalificacionModel).get_or_404(id)
        db.session.delete(calificacion)
        db.session.commit()
        return '',204

class Calificaciones(Resource):
    def get (self):
        calificaciones = db.session.query(CalificacionModel).all()
        return jsonify ([Calificacion.to_json_short() for calificacion in calificaciones])

    def post(self):
        calificacion = CalificacionModel.from_json(request.get_json())
        db.session.add(calificacion)
        db.session.commit()
        return calificacion.to_json(), 201