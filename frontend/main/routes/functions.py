from email import header
from urllib import response
from wsgiref import headers
from flask import Blueprint, url_for, render_template, make_response, request, current_app
import requests, json

def get_poem(id):
    api_url = f'{current_app.config["API_URL"]}/poema/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)

def get_poems(api_url, page=1, porpage=3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"page":page, "porpage":porpage}
    headers = get_headers()
    return requests.get(api_url, json=data, headers=headers)

def get_user_info(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    headers = get_headers()

    return requests.get(api_url, headers=headers)

def get_user(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    headers = get_headers()
    return requests.get(api_url, headers=headers)

def json_load(response):
    return json.loads(response.text)

def get_headers(without_token = False):
    jwt = get_jwt()
    if jwt and without_token == False:
        return{"Content-Type":"application/json", "Authorization":f"Bearer {jwt}"}
    else:
        return{"Content-Type":"application/json"}

def get_jwt():
    return request.cookies.get("access_token")

def get_id():
    return request.cookies.get("id")

def get_username(user_id):
    headers = get_headers
    api_url = f'{current_app.config["API_URL"]}/user/{user_id}'

def add_poem(api_url, titulo, contenido):
    data = {"titulo":titulo, "contenido":contenido}
    headers = get_headers()
    return request.post(api_url, json=data, headers = headers)

def login(email, password):
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    data = {"email": email, "password": password}
    headers = get_headers(without_token = True)

    return requests.post(api_url, json = data, headers = headers)