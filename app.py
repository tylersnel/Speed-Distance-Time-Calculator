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
            #data=int(speed)*int(time)
            #return render_template("distancecalc.j2", data=data)
    return render_template("distance.j2")
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 65234)) 
   
    
    app.run(port=port, debug=True)
