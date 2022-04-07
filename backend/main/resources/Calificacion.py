import resource
from flask_restful import Resource
from flask import request

#Calificaciones

CALIFICACIONES = {
    1:{'calificacion': '8','Autor':'Lun891'},
    2:{'calificacion': '10','Autor':'Juancito1991'},
}

class Calificacion(Resource):
    def get(self,id):
        if int(id) in CALIFICACIONES:
            return CALIFICACIONES[int(id)]
        return '',404
    def delete(self,id):
        if int(id) in CALIFICACIONES:
            del CALIFICACIONES[int(id)]
            return '',204
        return '',404

class Calificaciones(Resource):
    def get (self):
        return CALIFICACIONES

    def post(self):
        Calificacion = request.get_json()
        id = int(max(CALIFICACIONES.keys())) + 1
        CALIFICACIONES[id] = Calificacion
        return CALIFICACIONES[id], 201

