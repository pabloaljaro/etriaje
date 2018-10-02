from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app.forms import LoginForm
import json
import watson_developer_cloud


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home')


"""@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)"""
	

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    assistant = watson_developer_cloud.AssistantV1(
        username='3daff751-c00a-419c-9389-1dad623c85f8',
        password='0DgjskFGYC8H',
        version='2018-09-25'
    )

    message = ""
    response = assistant.message(
        workspace_id='732026f8-43b5-40cd-a98e-6081e7e869a2',
        encoding='utf-8',
        input={
            'text': message
        }
    ).get_result()

    saludo = json.dumps(response, indent=2)

    texto = response['output']['generic'][0]['text']
    context = response['context']
	
    return render_template('conversation.html',  bienvenida=texto, context=context)

@app.route('/interlocutor/', methods=['POST'])
def interlocutor():
	respuesta = {}
    
	if request.method == 'POST':
	
		user_talk = request.form.get("user_talk")
		maincontext = request.form.get("context")
		
		assistant = watson_developer_cloud.AssistantV1(
			username='3daff751-c00a-419c-9389-1dad623c85f8',
			password='0DgjskFGYC8H',
			version='2018-09-25'
		)


		response = assistant.message(
			workspace_id='732026f8-43b5-40cd-a98e-6081e7e869a2',
			encoding='utf-8',
			input={
				'text': user_talk
			},
			context= eval(maincontext)
		
		).get_result()

		saludo = json.dumps(response, indent=2)

		respuesta['respuesta_bot'] = response['output']['generic'][0]['text']
		respuesta['contexto_bot'] = response['context']
	
	#return Response(respuesta)
	return jsonify(respuesta)