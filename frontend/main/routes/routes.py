from email import header
from urllib import response
from flask import Blueprint, render_template, make_response, request, current_app
from . import functions as f
import requests
import json


app = Blueprint('app', __name__, url_prefix= '/')

@app.route('/poeta')
def index(jwt = None):
    
    if jwt == None:
        jwt =f.get_jwt()
    
    resp = f.get_poems(jwt=jwt)
    poems = f.get_json(resp)
    poem_list = poems["poemas"]
    user = f.get_user(f.get_id())
    user = json.loads(user.text)
    print(user)

    return render_template('pag_princ_poeta.html', poems = poem_list, user = user, jwt = jwt) 
    
    
    
    #return render_template ('pag_princ_poeta.html')
    #api_url = "http://127.0.0.1:8500/poemas"

    # data = {"page":1, "por_pagina":3}
    # jwt =requests.cookies.get("access_token")
    # print(jwt)
    # headers = {"Content-Type": "application/json", "Authorization": "BEARER {}".format(jwt)}
    # response = requests.get(api_url, json = data, headers = headers)
    # print(response.status_code)
    # poemas = json.loads(response.text)
    # print(poemas)

    # return render_template('pag_princ_poeta.html', poemas = poemas["poemas"])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == "POST"):
        # Obtener password y email
        email = request.form.get("email")
        password = request.form.get("contraseña")

        if email != None and password != None:
            response = f.login(email, password)
            
            if (response.ok):
                # Obtener el token desde response.
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])
                # Guardar el token en las cookies y devuelve la página.
                resp = make_response(index(jwt=token))
                #resp = make_response(redirect(url_for('main.index'), token))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)
                return resp
        return render_template("login.html", error = "Usuario y contraseña incorrectos")
    else:
        return render_template("login.html")

# @app.route('/')
# def index(jwt = None):
#     if (jwt == None):
#         jwt=f.get_jwt()
    
#     resp = f.get_poems(jwt = jwt)   

#     poems = f.get_json(resp)
#     list_poemas = poems["poems"]

#     return render_template('pag_princ_user.html',jwt = jwt, poems = list_poemas)


@app.route('/editar_perfil')
def editar_perfil():
    return render_template ('editar_perfil.html')

@app.route('/lista_poem_user')
def lista_poemas_usuario():
    return render_template ('lista_poem_user.html')

@app.route('/lista_poema_poeta')
def lista_poem_poeta():
    return render_template ('lista_poema_poeta.html')

@app.route('/user')
def index_user():
    api_url = f'{current_app.config["API_URL"]}/poemas'
    
    response = f.get_poems(api_url)

    print(response)
    poems = json.loads(response.text)
    list_poems = poems["poemas"]
    return render_template('pag_princ_user.html', poems=list_poems)

@app.route('/perfil')
def perfil():
    return render_template ('perfil.html')

@app.route('/subir_poema')
def subir_poema():
    return render_template ('subir_poema.html')

@app.route('/ver_poema_poeta')
def ver_poema_poeta():
    return render_template ('ver_poema_poeta.html')

@app.route('/ver_poema_user')
def ver_poema_user():
    return render_template ('ver_poema_user.html')