from flask import Blueprint, render_template, redirect, url_for,request,flash,session
from .forms import signupform, loginform,code,join
from .model import User,db,Active_room
from chatapp import login,login_user,login_required,logout_user,current_user,bcrypt
from flask_wtf import *
main = Blueprint("main", __name__)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@main.route("/create_room",methods=['GET', 'POST'])
def create_room():
    form=code()
    if not current_user.is_authenticated:
        flash('Please login', 'danger') 
        return render_template("404.html")
    if form.validate_on_submit():
        session["room_id"]=form.code.data
        user=User.query.filter_by(user_id=session["_user_id"]).first()
        if user:
            user.room_id=session["room_id"]
            new_room = Active_room(room_id=form.code.data, member_num=1)
            db.session.add(new_room)
            db.session.commit()

        return redirect(url_for('main.chat')) 

    return render_template("create_room.html",username=current_user.username,form=form)



@main.route("/join",methods=['GET', 'POST'])
def panel():
    form=join()
    if not current_user.is_authenticated:
        flash('Please login', 'danger') 
        return render_template("404.html")
    if form.validate_on_submit():
        user=User.query.filter_by(user_id=session["_user_id"]).first()
        if user:
            session["room_id"]=form.code.data
            user.room_id=form.code.data
            db.session.commit()

        flash('You have successfully joined the room.', 'success')

        return redirect(url_for('main.chat')) 

    return render_template("panel.html",form=form)


@main.route("/active_rooms", methods=['GET', 'POST'])
def rooms():
    all_users = Active_room.query.all()
    if all_users:
        return f"rooms{all_users}"
    else:
        return "not found"


@main.route("/accounts", methods=['GET', 'POST'])
def index():
    all_users = User.query.all()
    if all_users:
        return f"{all_users}"
    else:
        return "not found"
        

@main.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    room=session.get("room_id")
    if room is None:
        return redirect(url_for('main.login'))
    return render_template('room.html',username=current_user.username)

@main.route("/login", methods=['GET', 'POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.username.data)
            session['username']=form.username.data
            return redirect(url_for("main.panel"))
    return render_template("login.html", title='Login', form=form)

@main.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        redirect(url_for('main.signup'))
    form = signupform(request.form)
    if  form.validate_on_submit():
        username=form.username.data
        pasrd=form.password.data
        hashed_pswrd=bcrypt.generate_password_hash(pasrd).decode('utf-8')
        user=User(password=hashed_pswrd,username=username)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        # Redirect to a different page after successful registration
        return redirect(url_for('main.login'))  # Redirect to login page after signup
    return render_template("register.html", title='Register', form=form)

@main.route("/logout", methods=['GET', 'POST'])
def logout():
    flash('You have logged out sucessfully','success')
    logout_user()
    user=User.query.filter_by(username=session["username"]).first()
    if user:
        user.room_id=None
        db.session.commit()
        print(f"bye")
        return redirect(url_for('main.login')) 

    return redirect(url_for('main.login')) 




