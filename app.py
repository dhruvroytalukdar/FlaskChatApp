from flask import Flask, render_template, request, redirect,url_for
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = '5646addsknc'
socketio = SocketIO(app, cors_allowed_origins="*")

list_of_rooms = ['test'];

@app.route('/',methods=['POST','GET'])
def session():
    return render_template('session.html')


@socketio.on('message-pass')
def event_handler(json,methods = ['POST','GET']):
    print('Received message : ',str(json))
    if('user_name' in json.keys()):
        emit('display-client',{"user_name":json['user_name'],"message":json['message'],"roomcode":json['room']},room=json['room'])

@socketio.on('connect')
def connect_handler():
    print('someone connected')
    emit('new-user-update',{
        'list':list_of_rooms
    })

@socketio.on('join')
def join_handler(json):
    print(str(json),"join")
    if 'roomcode' in json.keys():
        username = json['username']
        roomID = json['roomcode']
    else:
        username = json['username']
        roomID = uuid.uuid1().hex
        list_of_rooms.append(roomID)
        socketio.emit('add-new-roomcode',{
            'code':roomID
        });
    join_room(roomID)
    emit("display-client",{"user_name":username,"message":"has entered the room","roomcode":roomID},room=roomID)


@socketio.on('leave')
def leave_room_handler(json):
    print(str(json),"leave")
    leave_room(json['room'])
    emit("display-client",{"user_name":json['username'],"message":"has left the room"},room=json['room'])

if __name__ == '__main__':
    socketio.run(app,debug = True,port=8080)
