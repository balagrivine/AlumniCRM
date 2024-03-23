from flask import Flask, reuqest, render_template

app = Flask(__name__)

@app.route('/')
def details():
    name = request.args.get('name')
    email = request.args.get('email')
    grad_year = request.args.get('grad_year')


