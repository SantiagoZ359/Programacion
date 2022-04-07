import resource
from flask_restful import Resource
from flask import request

#Poemas

POEMAS = {
    1:{'nombrepoema': 'Rafaga','Autor':'Lun891'},
    2:{'nombrepoema': 'La nueva luna','autor':'Juancito1991'},
}

class Poema(Resource):
    def get(self,id):
        if int(id) in POEMAS:
            return POEMAS[int(id)]
        return '',404
    def delete(self,id):
        if int(id) in POEMAS:
            del POEMAS[int(id)]
            return'',204
        return'',404

class Poemas(Resource):
    def get (self):
        return POEMAS
    def post(self):
        Poemas = request.get_json()
        id = int(max(POEMAS.keys())) + 1
        POEMAS[id] = Poema
        return POEMAS[id], 201
