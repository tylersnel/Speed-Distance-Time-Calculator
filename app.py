from flask import Flask
from flask import request
app=Flask(__name__)

@app.route('/')
def hello():
    return "Hello There"


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=3000, debug=True)
