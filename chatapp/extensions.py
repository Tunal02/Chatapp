from flask_socketio import SocketIO,send,emit,join_room,leave_room
sio=SocketIO()
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
import string
import random
def get_random_alphanumeric_string():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(4)))
    return result_str
result=get_random_alphanumeric_string()
