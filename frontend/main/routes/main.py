from urllib import response
from flask import Blueprint, redirect, render_template, url_for, make_response, request, current_app
import requests, json
from . import functions as f

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/poeta')
def index_poeta():
    api_url = f'{current_app.config["API_URL"]}'
    user_id = f.get_id()
    user = f.get_user(user_id)
    user = json.loads(user.text)

    jwt = f.get_jwt()
    response = f.get_poems(api_url)

    poemas = json.loads(response.text)
    list_poemas = poemas["poemas"]

    return render_template('pag_princ_poeta.html', user = user, jwt = jwt, poemas = list_poemas)

@main.route('/')
def index_user():
    api_url = f'{current_app.config["API_URL"]}/poemas'

    response = f.get_poems(api_url)
    print(response)

    poemas = json.loads(response.txt)
    list_poemas = poemas["poemas"]

    return render_template('pag_princ_user.html', poems = list_poemas)

@main.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        email = request.form.get("email")
        password = request.form.get("password")

        if email != None and password != None:
            api_url = f'{current_app.config["API_URL"]}/auth/login'
            data = {"email": email, "password":password}
            headers = {"Content-Type" : "application/json"}

            response = requests.post(api_url, json=data, headers=headers)

            if (response.ok):
                response = json.loads(response.text)
                token = response["access_token"]
                user_id = str(response["id"])

                api_url = f'{current_app.config["API_URL"]}'
                response = f.get_poems(api_url)

                poems = json.loads(response.text)
                list_poems = poems["poems"]
                user = f.get_user(user_id)
                user = json.loads(user.text)

                resp = make_response(render_template("pag_princ_poeta", poems=list_poems, user=user))
                resp.set_cookie("access_token", token)
                resp.set_cookie("id", user_id)

                return resp

        return render_template("login.html", error="Usuario o contraseña incorrectos")
    else:
        return render_template("login.html")
