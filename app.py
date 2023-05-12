from flask import Flask, request, render_template, redirect, session, url_for
import requests

from crawler import scrapePhImg
from db import TasksDb


app = Flask(__name__)
app.secret_key = 'INSERT SECRET KEY'

PROFILE_PSW = 'INSERT PASSWORD FOR LOGIN'

@app.route('/')
def homepage():

    if 'logged' in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        if request.values['password'] == PROFILE_PSW:
            session['logged'] = True
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=None )

    # return redirect(url_for('homepage'))

@app.route('/logout')
def logout():

    if 'logged' in session:
        session.pop('logged')
    return redirect(url_for('homepage'))

@app.route('/output', methods=['POST', 'GET'])
def output():

    if 'logged' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':

        link = request.values['link']
        desc = request.values['desc']

        error = None

        try:
            response = requests.get(link)
        except:
            error = True
            #errore poi gestito dal js        
            return "false"

        imagesrc = scrapePhImg(response)
            
        newtask = TasksDb()
        newtask.insert_task(link, imagesrc, desc)
        newtask.close()

        return render_template('output.html', data={
                                "link": link,
                                "response": response,
                                "error": error,
                                "imagesrc":imagesrc
                                })
    else:
        return redirect('/')
    
@app.route('/album')
def myalbum():
    if 'logged' not in session:
        return redirect(url_for('login'))
    
    db = TasksDb()
    tasks = db.get_tasks()

    # print(tasks)

    result = []

    for task in tasks:
        mydict = {}

        mydict['id'] = task[0]
        mydict['link'] = task[1]
        mydict['src'] = task[2]
        mydict['desc'] = task[3]
        mydict['date'] = task[4]

        result.append(mydict)

    # result = tasks

    return render_template('album.html', album=result)

if __name__ == "__main__":
    app.run(debug=True)

