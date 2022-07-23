from flask import Flask, render_template, request, redirect
import math
import os

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

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
            return render_template("distance.j2", data=data, measure=measure)
    return render_template("distance.j2")


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
            return render_template("speed.j2", data=data, measure=measure)
    return render_template("speed.j2")

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
            seconds_float=seconds_holder*60
            seconds=math.trunc(seconds_float)


            

            data=round(int(distance)/int(speed), 3)
            return render_template("time.j2", data=data, measure=measure)
    return render_template("time.j2")

@app.route('/advanced')
def advanced():
    return render_template("advanced.j2")
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 65234)) 
   
    
    app.run(port=port, debug=True)
