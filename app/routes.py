from flask import render_template, request, redirect,url_for
from flask_socketio import join_room, leave_room, send, emit
import uuid
from app import app
from app import socketio
from .models import *
from app import db

users = {"123456abcderfghi"}

@app.route('/',methods=['POST','GET'])
def session():
    return render_template('session.html')


@socketio.on('message-pass')
def event_handler(json,methods = ['POST','GET']):
    print('Received message : ',str(json))

    m = Message(sender=json['user_name'],message_content=json['message'],room_id=Room.query.filter_by(room_key=json['room']).first().room_id)
    db.session.add(m)
    db.session.commit()

    room = Room.query.filter_by(room_key=json['room']).first()


    if('user_name' in json.keys()):
        emit('display-client',{"user_name":json['user_name'],"message":json['message'],"roomcode":json['room'],"id":m.message_id,"members":room.members},room=json['room'])



@socketio.on('check-room')
def check_room_handler(json):
    print(str(json))
    if db.session.query(Room).filter_by(room_key=json['room_id']).first() == None :
        print("False")
        emit('if-room',{'present':False,'user':json['username'],'error':'Room with this code does not exits'})
    elif json['username'] in users:
        print('False duplicate username')
        emit('if-room',{'present':False,'user':json['username'],'error':'This user already exists.Try another name.'})    
    else:
        print("True")
        users.add(json['username'])
        room = Room.query.filter_by(room_key=json['room_id']).first()
        list = []
        for messages in Message.query.filter_by(room_id=room.room_id).all():
            list.append({'user':messages.sender,'message':messages.message_content,'id':messages.message_id})
        emit('if-room',{'present':True,'user':json['username'],'message_list':list,"members":room.members+1})


@socketio.on('join')
def join_handler(json):
    print(str(json),"join")
    room = ""
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
        users.add(json['username'])
        socketio.emit('add-new-roomcode',{
            'code':roomID
        });
    join_room(roomID)
    room = Room.query.filter_by(room_key=roomID).first()
    emit("display-client",{"user_name":username,"message":"has entered the room","roomcode":roomID,"id":"temp","members":room.members},room=roomID)

@socketio.on('delete-message')
def delete_message_handler(json):
    Message.query.filter_by(message_id=int(json["id"])).delete()
    db.session.commit()
    emit("remove-message",{"id":json["id"]},room=json["room"])


@socketio.on('leave')
def leave_room_handler(json):
    print(str(json),"leave")
    room = db.session.query(Room).filter_by(room_key=json['room']).first()
    room.members -= 1
    users.remove(json['username'])
    print("Room :",room)
    if room.members == 0:
        Room.query.filter_by(room_id=room.room_id).delete()
    db.session.commit()   
    if room.members != 0:
        emit("display-client",{"user_name":json['username'],"message":"has left the room","members":room.members,"id":"temp"},room=json['room'])
    leave_room(json['room'])
   