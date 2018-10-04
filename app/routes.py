# encoding=utf8
from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import LoginForm
import json
import ibm_db
from ibm_db import fetch_assoc, tables, exec_immediate
from app.functions import watsonConnection


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

    respuesta['respuesta_bot'] = response['output']['generic'][0]['text']
    respuesta['contexto_bot'] = response['context']

    # return Response(respuesta)
    return jsonify(respuesta)


@app.route('/prueba', methods=['GET', 'POST'])
def prueba():
    # Documentacion python - bbdd en https://www.ibm.com/support/knowledgecenter/es/SSEPGG_9.5.0/com.ibm.db2.luw.apdv.python.doc/doc/t0054388.html
    conn = ibm_db.connect(
        "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=jnw52971;PWD=ft0d3qpf+q1whs7n;", "", "")
    sql = 'SELECT * FROM JNW52971.USUARIO'
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    output = ""
    while dictionary != False:
        output += str(dictionary['ID_USER']) + " - " + \
            str(dictionary['NOMBRE_USUARIO']) + "<br>"
        dictionary = ibm_db.fetch_both(stmt)

    ibm_db.close(conn)

    return output
