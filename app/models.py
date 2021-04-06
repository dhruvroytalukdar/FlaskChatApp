from app import db
from datetime import datetime

class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(40),unique=False,nullable=False)
    message_content = db.Column(db.Text,nullable=False)
    time_stamp = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    room_id = db.Column(db.Integer,db.ForeignKey('room.room_id',ondelete="CASCADE"),nullable=False)

    def __repr__(self):
        return f"Message('{self.sender} on '{self.time_stamp}')"

class Room(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    room_key = db.Column(db.String(50),nullable=False,unique=True)
    members = db.Column(db.Integer,default=0)
    messages = db.relationship('Message',backref='room',lazy=True)

    def __repr__(self):
        return f"Room('{self.room_id}' with '{self.members}'  members)"