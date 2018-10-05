# encoding=utf8
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import LoginForm
import json
import ibm_db
from ibm_db import fetch_assoc, tables, exec_immediate
from app.functions import watsonConnection, insertarUsuarios, insertarAnalisis, updateAnalisis


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    categoria = str(request.args.get('cat'))
    response = watsonConnection("", json.dumps(
        {'conversation_id': '0'}, indent=2), categoria)
    saludo = json.dumps(response, indent=2)

    texto = response['output']['generic'][0]['text']
    context = response['context']

    titulo = ''
    if categoria == 'st':
        titulo = 'Síntomas'
    else:
        titulo = 'Análisis'
    return render_template('conversation.html',  bienvenida=texto, context=context, titulo=titulo, categoria=categoria)


@app.route('/interlocutor/', methods=['POST'])
def interlocutor():

    respuesta = {}

    if request.method == 'POST':

        user_talk = request.form.get("user_talk")
        maincontext = request.form.get("context")
        categoria = request.form.get("cat")
        response = watsonConnection(user_talk, maincontext, categoria)
    
    saludo = json.dumps(response, indent=2)
    #print(saludo)
    respuesta['respuesta_bot'] = response['output']['generic'][0]['text']
    #print(type(respuesta['respuesta_bot']))
    aux = ''
    if len(respuesta['respuesta_bot']) > 1:
        for r in respuesta['respuesta_bot']:
            aux += r
        respuesta['respuesta_bot'] = aux

    respuesta['contexto_bot'] = response['context']

    # return Response(respuesta)
    return jsonify(respuesta)


@app.route('/iuser', methods=['GET', 'POST'])
def iuser():
    result = ""
    if request.method == 'POST':
        tx_usuario = request.form.get("tx_usuario")
        tx_password = request.form.get("tx_nombre")
        result = insertarUsuarios(tx_usuario,tx_password)
    return result

@app.route('/ianalisis', methods=['GET', 'POST'])
def ianalisis():
    result = ""
    if request.method == 'POST':
        user = request.form.get("ID_USUARIO")
        tipoanalisis = request.form.get("CO_TIPO_ANALISIS")
        fecha = request.form.get("FE_FECHA_ANALISIS")
        result = insertarUsuarios(user,tipoanalisis,fecha)
    return result