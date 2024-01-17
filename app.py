from flask import Flask, render_template, request, redirect

# from flask_ngrok import run_with_ngrok

app = Flask(__name__)


# run_with_ngrok(app)
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/hobby")
def hobby():
    return render_template('hobby.html')


@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/shoutout")
def shoutout():
    return render_template('shoutout.html')


app.run()
