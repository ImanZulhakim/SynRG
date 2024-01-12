from flask import Flask, render_template, request, redirect
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/iman")
def iman():
    return render_template('iman.html')

@app.route("/hobby")
def hobby():
    return render_template('hobby.html')


app.run()


