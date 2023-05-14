from flask import Flask, redirect, render_template, request, session, url_for

from admin_page import admin_page

import db

app = Flask(__name__, )
app.secret_key = 'INSERT SECRET KEY'

PROFILE_PSW = 'INSERT PASSWORD'

app.config['session'] = session
app.config['PROFILE_PSW'] = PROFILE_PSW

app.register_blueprint(admin_page)

@app.route('/')
def homepage():
    return render_template('/public/index.html')

if __name__ == "__main__":
    app.run(debug=True)

