from .extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    room_id = db.Column(db.String, db.ForeignKey('active_room.room_id'), nullable=True)
    room = db.relationship('Active_room', backref='users')
    def get_id(self):
           return (self.user_id)
    
    def __repr__(self):
        return f"Active_room(user={self.user_id},username={self.username},room_id={self.room_id})"


class Active_room(UserMixin,db.Model):
    __tablename__ = 'active_room'
    room_id = db.Column(db.String, primary_key=True,nullable=True)
    member_num = db.Column(db.Integer, nullable=False, default=0)
    message = db.Column(db.Text)

    def __repr__(self):
        return f"Active_room(room_id={self.room_id}, member_num={self.member_num})"
