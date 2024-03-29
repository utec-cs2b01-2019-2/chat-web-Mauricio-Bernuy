from flask import Flask,render_template, request, session, Response, redirect

from os import environ
from database import connector
from model import entities

import datetime
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
app.secret_key = ".."

@app.route('/')
def index():
    db_session = db.getSession(engine)
    if 'logged_user' in session:
        users = db_session.query(entities.User).filter(entities.User.id == (session['logged_user']))
        for user in users:
            return render_template('index.html', name = user.name)
    else:
        return render_template('login.html', name = 'Log in to your account')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    return "Deleted User"

@app.route('/create_test_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user = entities.User(name="David", fullname="Lazo", password="1234", username="qwerty")
    db_session.add(user)
    db_session.commit()
    return "Test user created!"

@app.route('/messages', methods = ['POST'])
def create_message():
    c = json.loads(request.form['values'])
    message = entities.Message(
        content=c['content'],
        sent_on=datetime.datetime(2000,2,2),
        user_from_id=c['user_from_id'],
        user_to_id=c['user_to_id']
    )
    session = db.getSession(engine)
    session.add(message)
    session.commit()
    return 'Created Message'

@app.route('/messages/<id>', methods = ['GET'])
def get_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(js, status=200, mimetype='application/json')

    message = {'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

@app.route('/messages', methods = ['GET'])
def get_messages():
    sessionc = db.getSession(engine)
    dbResponse = sessionc.query(entities.Message)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages/<user_from_id>/<user_to_id>', methods = ['GET'])
def get_messages_user(user_from_id, user_to_id ):
    db_session = db.getSession(engine)
    messages_send = db_session.query(entities.Message).filter(
        entities.Message.user_from_id == user_from_id).filter(
        entities.Message.user_to_id == user_to_id
    )
    messages_recieved = db_session.query(entities.Message).filter(
        entities.Message.user_from_id == user_to_id).filter(
        entities.Message.user_to_id == user_from_id
    )
    data = []
    for message in messages_send:
        data.append(message)
    for message in messages_recieved:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'

@app.route('/messages', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    message = session.query(entities.Message).filter(entities.Message.id == id).one()
    session.delete(message)
    session.commit()
    return "Deleted Message"

@app.route('/create_test_messages', methods = ['GET'])
def create_test_messages():
    db_session = db.getSession(engine)
    message = entities.Message(content="Hi")
    db_session.add(message)
    db_session.commit()
    return "Test message created!"

@app.route('/sendMessage', methods = ['POST'])
def send_message():
    message = json.loads(request.data)
    content = message['content']
    user_from_id = message['user_from_id']
    user_to_id = message['user_to_id']
    session = db.getSession(engine)
    add = entities.Message(
    content=content,
    sent_on=datetime.datetime(2000, 2, 2),
    user_from_id=user_from_id,
    user_to_id=user_to_id,

    )
    session.add(add)
    session.commit()
    return 'Message sent'

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    #Get data form request
    message = json.loads(request.data)
    username = message['username']
    password = message['password']

    # Look in database
    db_session = db.getSession(engine)

    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username==username
            ).filter(entities.User.password==password
            ).one()

        session['logged_user'] = user.id
        message = {'message':'Authorized'}
        message = {'message':'Authorized', 'user_id': user.id, 'username': user.username}
        return Response(json.dumps(message,cls=connector.AlchemyEncoder), status=200,mimetype='application/json')
    except Exception:
        message = {'message':'Unauthorized'}
        return Response(json.dumps(message,cls=connector.AlchemyEncoder), status=401,mimetype='application/json')


@app.route('/current', methods = ['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == session['logged_user']).first()
    return Response(json.dumps(user,cls=connector.AlchemyEncoder),mimetype='application/json')

#API de GRUPOS
#1.CREATE
@app.route('/groups', methods = ['POST'])
def create_group():
    c = json.loads(request.data)
    group = entities.Group(name=c['name'])
    session_db = db.getSession(engine)
    session_db.add(group)
    session_db.commit()
    return 'Created Group'
#2.READ
@app.route('/groups/<id>', methods = ['GET'])
def read_group(id):
    group = session_db.query(entities.Group).filter(entities.Group.id ==id).first()
    data = json.dumps(group, cls=connector.AlchemyEncoder)
    return Response (data, status=200, mimetype='application/json')


@app.route('/groups', methods = ['GET'])
def get_all_groups():
    session_db = db.getSession(engine)
    dbResponse = session_db.query(entities.Group)
    data = dbResponse[:]
    return Response(json.dumps(data,cls=connector.AlchemyEncoder), mimetype='application/json')

#UPDATE
@app.route('/groups/<id>', methods = ['PUT'])
def update_group():
    session = db.getSession(engine)
    group = session_db.query(entities.Group).filter(entities.Group.id ==id).first()
    c = json.loads(request.data)
    for key in c.keys():
        setattr(group, key, c[key])
    session_db.add(group)
    session_db.commit()
    return 'Updated Group'

#DELETE
@app.route('/groups/<id>', methods = ['DELETE'])
def delete_group(id):
    session = db.getSession(engine)
    group = session_db.query(entities.Group).filter(entities.Group.id == id).one()
    session.delete(group)
    session.commit()
    return "Deleted Group"

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return render_template('login.html')

#stateless interaction
@app.route('/cuantasletras/<nombre>')
def cuantas_letras(nombre):
    return str(len(nombre))

#stateful interaction
@app.route('/suma/<numero>')
def suma(numero):
    if 'suma' not in session:
        session['suma'] = 0

    suma = session['suma']
    suma = suma + int(numero)
    session[suma]=suma
    return str(suma)


if __name__ == '__main__':
    app.run(debug=True,port=8000, threaded=True, use_reloader=False)
