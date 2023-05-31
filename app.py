from flask import Flask, redirect, render_template, request, session, url_for

from admin_page import admin_page

import db
import json, os

app = Flask(__name__, )

if not os.path.isfile('credentials.json'):
    print('Credenziali mancanti. Creare file credentials.json')

with open('credentials.json', 'r') as file:
    data = file.read()

dataJson = json.loads(data)

secret_key_session = dataJson['secret_key_session']
app.secret_key = secret_key_session

app.config['session'] = secret_key_session
app.config['PROFILE_PSW'] = dataJson['PROFILE_PSW']

app.register_blueprint(admin_page)

@app.route('/')
def homepage():
    return render_template('/public/index.html')

if __name__ == "__main__":
    app.run(debug=True)

