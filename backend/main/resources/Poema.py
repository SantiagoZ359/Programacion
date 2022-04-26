from flask_restful import Resource
from flask import request, jsonify
from main.models import PoemaModel
from .. import db

#Poemas

#POEMAS = {
#    1:{'nombrepoema': 'Rafaga','Autor':'Lun891'},
#    2:{'nombrepoema': 'La nueva luna','autor':'Juancito1991'},
#}

class Poema(Resource):
    def get(self,id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        return poema.to_json()
    def delete(self,id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        db.session.delete(poema)
        db.session.commit()
        return '',204

class Poemas(Resource):
    def get (self):
        poemas = db.session.query(PoemaModel)
        #definimos en que pag estamos
        pagina = 1
        #cuatos objetos mostramos por pag
        por_pagina = 5
        #definimos el request y los filtros
        if request.get_json():
            filtros = request.get_json().items()
            for key, valor in filtros:
                if key == "pagina":
                    pagina = int(valor)
                if key == "por_pagina":
                    por_pagina = int(valor)
        poemas = poemas.paginamiento(pagina,por_pagina, True, 10)
        return jsonify ({"poemas":[poema.to_json_short() for poema in poemas.items()],
        "total": poemas.total, "paginas": poemas.paginas, "pagina": pagina})

    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201