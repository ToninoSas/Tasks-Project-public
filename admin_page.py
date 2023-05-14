from flask import Blueprint, render_template, abort, redirect, url_for, current_app, request
from jinja2 import TemplateNotFound

import requests

from crawler import scrapePhImg
from db import TasksDb

admin_page = Blueprint('admin_page', __name__, static_folder='static', template_folder='templates/admin')

@admin_page.route('/admin')
def show():
    session = current_app.config['session']

    if 'logged' not in session:
        return redirect(url_for('admin_page.login'))

    return render_template('index.html')

@admin_page.route('/admin/login', methods=['POST', 'GET'])
def login():

    session = current_app.config['session']
    PROFILE_PSW = current_app.config['PROFILE_PSW']

    if 'logged' in session:
        return redirect(url_for('admin_page.show'))

    if request.method == 'POST':
        
        if request.values['password'] == PROFILE_PSW:
            session['logged'] = True
            return redirect(url_for('admin_page.show'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=None )

@admin_page.route('/admin/logout')
def logout():
    session = current_app.config['session']

    if 'logged' in session:
        session.pop('logged')
    return redirect(url_for('homepage'))

@admin_page.route('/admin/save', methods=['POST', 'GET'])
def output():

    session = current_app.config['session']

    if 'logged' not in session:
        return redirect(url_for('admin_page.login'))
    
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

        return render_template('response.html', data={
                                "link": link,
                                "response": response,
                                "error": error,
                                "imagesrc":imagesrc
                                })
    else:
        return redirect(url_for('homepage'))
    
@admin_page.route('/admin/album')
def album():

    session = current_app.config['session']

    if 'logged' not in session:
        return redirect(url_for('admin_page.login'))
    
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