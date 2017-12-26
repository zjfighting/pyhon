#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import json
from flask import Flask, render_template, abort

app = Flask(__name__)

def getTitles(filename):
    print(filename)
    titles = []
    for name in os.listdir(filename):
        print(name)
        kuozhanming = name.split('.')[-1]
        if(kuozhanming == 'json'):
            fname = filename + '/' + name
            with open(fname, 'r') as file:
                news = json.loads(file.read())
                title = news['title']
                titles.append(title)
    return titles
@app.route('/')
def index():
    filename = '/home/shiyanlou/files/'
    titles = getTitles(filename)
    for title in titles:
        print(title)
    return render_template('index.html', titles=titles)


@app.route('/files/<filename>')
def getContent(filename):
    name = '/home/shiyanlou/files/' + filename + '.json'
    flag = os.path.exists(name)
    if(flag == False):
        print("404")
        abort(404)
    else:
        with open(name, 'r') as file:
            news = json.loads(file.read())
            content = news['content']
            print(content)
    return render_template('file.html', content=content)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

