import resource
from flask_restful import Resource
from flask import request

#Poemas

POEMAS = {
    1:{'nombrepoema': 'Rafaga','Autor':'Lun891'},
    2:{'nombrepoema': 'La nueva luna','autor':'Juancito1991'},
}

class Poema(resource):
    def get(self,id):
        if int(id) in POEMAS:
            return POEMAS[int(id)]
        return '',404
    def post(self,id):
        if int(id) in POEMAS:
            return POEMAS[int(id)]
        return '',404