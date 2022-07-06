from flask import Flask, render_template, request, redirect

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

            #convert time that is a string to integers
            hh=time[0]+time[1] 
            hh=int(hh)
            mm=time[3]+time[4]
            mm=int(mm)
            ss=time[6]+time[7]
            ss=int(ss)

            #convert to decimal for calculation
            time=hh+(mm/60)+(ss/3600)
            time=round(time , 3)

            data=int(speed)*time
            return render_template("distance.j2", data=data)
    return render_template("distance.j2")
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 65234)) 
   
    
    app.run(port=port, debug=True)
