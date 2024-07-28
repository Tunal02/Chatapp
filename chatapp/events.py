from .extensions import sio,send,emit,join_room,leave_room


@sio.on('message')
def handle_message(data):
    from .routes import  session
    from chatapp import current_user
    username=current_user.username
    print(session.get("username"))
    room = session.get("room_id")
    if room:
    # Broadcast message to all clients in the room
        emit('message', {'username': username, 'message': data['message']}, room=room)
   
@sio.on("connect")
def handle_connect():
    from .routes import  session
    from chatapp import current_user
    
    name=current_user.username
    room=session.get("room_id")
    if room:
        join_room(room)
        emit('join',{'name':name,'message':"has entered the room"},broadcast=True,room=room)
        print(f"{name}  connected to room {room}")

@sio.on('leave')
def leave():
    from .routes import session,User,db,url_for
    name=session.get("username")
    room=session.get("room_id")
    if room:
        leave_room(room)
        emit('leave',{'name':name,'message':"has left the room"},room=room)
        user=User.query.filter_by(user_id=session["_user_id"]).first()
        if user:
            user.room_id=None
            db.session.commit()
            print(f"{name}  left the  room {room}")

            emit('redirect', {'url': url_for('main.login')}, broadcast=True)



