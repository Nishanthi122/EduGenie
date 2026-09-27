from flask import Flask

app = Flask("EduGenie")

@app.route('/')

def home():
     
     return "EduGenie is RunningSuccessfully!"

app.run(debug=True)
