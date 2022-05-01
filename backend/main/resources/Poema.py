from datetime import *
from flask_restful import Resource
from flask import request, jsonify
from main.models import PoemaModel, UsuarioModel
from sqlalchemy import func
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
    def put(self,id):
        poema = db.session.query(PoemaModel).get_or_404(id)
        data = request.get_json().items()
        for key, valor in data:
            setattr(poema,key,valor)
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201


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
                if key == 'pagina':
                    pagina = int(valor)
                #elementos que va a mostrar por pag
                if key == 'por_pagina':
                    por_pagina = int(valor)
                #filtro titulo del poema
                if key == 'titulo':
                    poemas == poemas.filtro(PoemaModel.titulo.like('%'+valor+'%'))
                #filtro id del autor
                if key == 'usuario_id':
                    poemas = poemas.filtro(PoemaModel.usuario_id == valor)
                #filtro fecha gte
                if key == 'fecha[gt]':
                    poemas == poemas.filtro(PoemaModel.fecha >= datetime.strftime(valor, '%d-%m-%Y'))
                #filtro fecha lte
                if key == 'fecha[lt]':
                    poemas == poemas.filtro(PoemaModel.fecha <= datetime.strftime(valor, '%d-%m-%Y'))
                #filtro nombre del autor
                if key == 'nombre_usuario':
                    poemas == poemas.filtro(PoemaModel.usuario.has(UsuarioModel.username.like('%'+valor+'%')))

                #Ordentamiento
                if key == "ordenar_por":
                    #Ordenamiento por fechas ascendete
                    if valor == 'fecha_hora':
                        poemas = poemas.order_by(PoemaModel.fecha_hora)
                    #Ordenamiento por fechas descendente
                    if valor == 'fecha_hora[desc]':
                        poemas == poemas.order_by(PoemaModel.fecha_hora.desc())
                    #Ordenamiento por promedio de calificaciones
                    if valor == 'nota':
                        poemas == poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.prom(PoemaModel.media_calificaciones))
                    #Ordenamiento por promedio de calificaciones decendente
                    if valor == 'nota[desc]':
                        poemas == poemas.outerjoin(PoemaModel.calificaciones).group_by(PoemaModel.id).order_by(func.prom(PoemaModel.media_calificaciones).desc())
                    #Ordenamiento por nombre de autor ascendente
                    if valor == 'nombre_autor':
                        poemas == poemas.order_by(PoemaModel.usuario)
                    #Ordenamiento por nombre de autor descendente
                    if valor == 'nombre_autor[desc]':
                        poemas == poemas.order_by(PoemaModel.usuario.desc())

        poemas = poemas.paginamiento(pagina,por_pagina, True, 10)
        return jsonify ({"poemas":[poema.to_json_short() for poema in poemas.items()],
        "total": poemas.total, "paginas": poemas.paginas, "pagina": pagina})

    def post(self):
        poema = PoemaModel.from_json(request.get_json())
        db.session.query(PoemaModel).get_or_404(poema.usuario_id)
        db.session.add(poema)
        db.session.commit()
        return poema.to_json(), 201