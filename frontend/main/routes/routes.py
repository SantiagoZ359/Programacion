from flask import Blueprint, render_template


app = Blueprint('app', __name__, url_prefix= '/')

@app.route('/poeta')
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