from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,  login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import zmq
import math
import os

# Configuration
context = zmq.Context()



app = Flask(__name__)
db= SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
bcrypt=Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


#get images from microservice server
print("Connecting server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
da_list=['distance', 'speed', 'pace']
from_server=[]
for url_req in da_list:
    print(f"Sending request {url_req} …")
    socket.send_string(url_req)



    #  Get the reply.
    message = socket.recv()
    print(f"Received {message} ")
    message=message.decode("utf-8")
    from_server.append(message)

distance_img=from_server[0]
speed_img=from_server[1]
time_img=from_server[2]

    

# Routes 

@app.route('/', methods=['GET', 'POST'])
def root():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/distance')

    return render_template("main.j2", form=form)

@app.route('/register', methods=['GET', 'POST' ])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    return render_template("register.j2", form=form)

@app.route('/distance', methods=["POST", "GET"])
def distance():
    if request.method=="POST":
        if request.form.get ('userInput'):
            speed=request.form['speed']
            time=request.form['time']
            unit=request.form['unit']
            

            if unit=="km":
                measure="kilometers"
            else:
                measure="miles"
            

            #convert time that is a string to integers
            hh=time[0]+time[1] 
            hh=int(hh)
            mm=time[3]+time[4]
            mm=int(mm)
            ss=time[6]+time[7]
            ss=int(ss)

            #convert to decimal for calculation
            time=hh+(mm/60)+(ss/3600)
            

            data=round(int(speed)*time, 3)
            return render_template("distance.j2", data=data, measure=measure,distance_img=distance_img)
    return render_template("distance.j2", distance_img=distance_img)


@app.route('/speed', methods=["POST", "GET"])
def speed():
    if request.method=="POST":
        if request.form.get ('userInput'):
            distance=request.form['distance']
            time=request.form['time']
            unit=request.form['unit']

            if unit=="Kilometers":
                measure="kph"
            else:
                measure="mph"
            

            #convert time that is a string to integers
            hh=time[0]+time[1] 
            hh=int(hh)
            mm=time[3]+time[4]
            mm=int(mm)
            ss=time[6]+time[7]
            ss=int(ss)

            #convert to decimal for calculation
            time=hh+(mm/60)+(ss/3600)
            

            data=round(int(distance)/time, 3)
            return render_template("speed.j2", data=data, measure=measure, speed_img=speed_img)
    return render_template("speed.j2", speed_img=speed_img)

@app.route('/time', methods=["POST", "GET"])
def time():
    if request.method=="POST":
        if request.form.get ('userInput'):
            distance=request.form['distance']
            speed=request.form['speed']
            #convert to int for calculation
            distance=int(distance)
            speed=int(speed)

            time=distance/speed

            hours=math.trunc(time)

            minutes_holder=time-hours
            minutes_float=minutes_holder*60
            minutes=math.trunc(minutes_float)

            seconds_holder=minutes_float-minutes
            seconds_float=round(seconds_holder*60)
            seconds=math.trunc(seconds_float)

            hours=str(hours)
            if len(hours)==1:
                hours="0"+hours

            minutes=str(minutes)
            if len(minutes)==1:
                minutes="0"+minutes

            seconds=str(seconds)
            if len(seconds)==1:
                seconds="0"+seconds
            

            data= (hours+":"+minutes+":"+seconds)
            return render_template("time.j2", data=data, time_img=time_img)
    return render_template("time.j2", time_img=time_img)

@app.route('/advanced')
def advanced():
    return render_template("advanced.j2")
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 65234)) 
   
    
    app.run(port=port, debug=True)
