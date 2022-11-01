from email import header
from urllib import response
from flask import Blueprint, render_template, make_response, request
from . import functions as f
import requests
import json


app = Blueprint('app', __name__, url_prefix= '/')

@app.route('/poeta')
def index():
    #return render_template ('pag_princ_poeta.html')
    api_url = "http://127.0.0.1:8500/poemas"

    data = {"page":1, "por_pagina":3}
    jwt =requests.cookies.get("access_token")
    print(jwt)
    headers = {"Content-Type": "application/json", "Authorization": "BEARER {}".format(jwt)}
    response = requests.get(api_url, json = data, headers = headers)
    print(response.status_code)
    poemas = json.loads(response.text)
    print(poemas)

    return render_template('pag_princ_poeta.html', poemas = poemas["poemas"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")

        if email != None and password != None:

            response = f.login(email,password)

            if (response.ok):
                response = json.loads(response.text)
                token = response["access_token"]
                
                resp = make_response(index(jwt=token))
                resp.set_cookie("access_token", token)
                return resp

        return render_template("pag_princ_poeta.html")
    else:
        return render_template("login.html")

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
def pag_princ_user():
    return render_template ('pag_princ_user.html')

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