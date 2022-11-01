from urllib import response
from flask import Blueprint, redirect, render_template, url_for, make_response, request, current_app
import requests, json
from . import functions as f

main = Blueprint('main', __name__, url_prefix='/')

# # @main.route('/poet')
# # def index_poeta():
# #     api_url = f'{current_app.config["API_URL"]}'
# #     user_id = f.get_id()
# #     user = f.get_user(user_id)
# #     user = json.loads(user.text)

# #     jwt = f.get_jwt()
# #     response = f.get_poems(api_url)

# #     poemas = json.loads(response.text)
# #     list_poemas = poemas["poemas"]

# #     return render_template('pag_princ_poeta.html', user = user, jwt = jwt, poemas = list_poemas)

@main.route('/')
def index(jwt = None):
    if (jwt == None):
        jwt=f.get_jwt()
    
    resp = f.get_poems(jwt = jwt)

    poems = f.get_json(resp)
    list_poemas = poems["poems"]

    return render_template('pag_princ_user.html',jwt = jwt, poems = list_poemas)


@main.route("/login", methods=["GET", "POST"])
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

        return render_template("login.html")
    else:
        return render_template("login.html")
