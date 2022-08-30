from flask import Blueprint, render_template


app = Blueprint('app', __name__, url_prefix= '/')

@app.route('/')
def index():
    return render_template ('pag_princ_poeta.html')

@app.route('/login')
def login():
    return render_template ('login.html')

@app.route('/editar_perfil')
def editar_perfil():
    return render_template ('editar_perfil.html')

@app.route('/lista_poem_user')
def lista_poemas_usuario():
    return render_template ('lista_poem_user.html')

@app.route('/lista_poem_poeta')
def lista_poem_poeta():
    return render_template ('lista_poema_poeta.html')
