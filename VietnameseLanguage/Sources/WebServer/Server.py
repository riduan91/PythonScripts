#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
   return "Ceci est la page d'accueil."
   
@app.route('/hello/<phrase>')
def hello(phrase):
   htmlpage = "<h1>%s</h1>" % phrase
   return htmlpage

@app.route('/contact', methods = ['GET'])
def contact():
   return "formulaire"
   
@app.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number %d' % postID
    
@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' % guest
    
@app.route('/admin')
def hello_admin():
    return 'Hello Admin'
    
@app.route('/user/<name>')
def hello_user(name):
    if name=='admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest', guest=name))

@app.route('/success/<name>')
def success(name):
    return 'Welcome %s' % name

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('name')
        return redirect(url_for('success', name=user))

port = 8800
if __name__ == '__main__':
    app.run(port = 8800, debug=True)