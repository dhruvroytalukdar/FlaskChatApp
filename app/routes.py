from flask import render_template, request, redirect,url_for
from flask_socketio import join_room, leave_room, send, emit
import uuid
from app import app
from app import socketio
from .models import *
from app import db


@app.route('/',methods=['POST','GET'])
def session():
    return render_template('session.html')


@socketio.on('message-pass')
def event_handler(json,methods = ['POST','GET']):
    print('Received message : ',str(json))

    db.session.add(Message(sender=json['user_name'],message_content=json['message'],room_id=Room.query.filter_by(room_key=json['room']).first().room_id))
    db.session.commit()

    if('user_name' in json.keys()):
        emit('display-client',{"user_name":json['user_name'],"message":json['message'],"roomcode":json['room']},room=json['room'])



@socketio.on('check-room')
def check_room_handler(json):
    print(str(json))
    if db.session.query(Room).filter_by(room_key=json['room_id']).first() == None :
        print("False")
        emit('if-room',{'present':False,'user':json['username']})
    else:
        print("True")

        room = Room.query.filter_by(room_key=json['room_id']).first()
        list = []
        for messages in Message.query.filter_by(room_id=room.room_id).all():
            list.append({'user':messages.sender,'message':messages.message_content})
        emit('if-room',{'present':True,'user':json['username'],'message_list':list})


@socketio.on('join')
def join_handler(json):
    print(str(json),"join")
    if 'roomcode' in json.keys():
        username = json['username']
        roomID = json['roomcode']
        room = db.session.query(Room).filter_by(room_key=roomID).first()
        room.members += 1
        db.session.commit()
        print('Room :',room)
    else:
        username = json['username']
        roomID = uuid.uuid1().hex
        #list_of_rooms.append(roomID)
        db.session.add(Room(room_key=roomID,members=1))
        db.session.commit()
        socketio.emit('add-new-roomcode',{
            'code':roomID
        });
    join_room(roomID)
    emit("display-client",{"user_name":username,"message":"has entered the room","roomcode":roomID},room=roomID)


@socketio.on('leave')
def leave_room_handler(json):
    print(str(json),"leave")
    room = db.session.query(Room).filter_by(room_key=json['room']).first()
    room.members -= 1
    print("Room :",room)
    if room.members == 0:
        Room.query.filter_by(room_id=room.room_id).delete()
    db.session.commit()   
    if room.members != 0:
        emit("display-client",{"user_name":json['username'],"message":"has left the room"},room=json['room'])
    leave_room(json['room'])
   