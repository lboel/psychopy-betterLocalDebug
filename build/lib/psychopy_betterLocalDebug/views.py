# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response, send_from_directory, jsonify,redirect,url_for,session
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from psychopy_betterLocalDebug import app

app.secret_key = 'dev'
resource_path = Path(__file__).parent
GlobalPath =""


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Please use 127.0.0.1:5000/add/EXPERIMENTPATH to start an experiment"

@app.route('/add/<path:systemPath>', methods=['GET', 'POST'])
def addExperiments(systemPath):
    session["path"] = systemPath
    return redirect(url_for('experiments', shortPath=os.path.basename(systemPath)+"/"))

@app.route('/experiments/<path:shortPath>', methods=['GET', 'POST'])
def experiments(shortPath):
    lines = [session.get("path")]
    tailList = []
    for path in lines:
        head2, tail2 = os.path.split(path)
        tailList.append(tail2+"/index.html")
    head, tail = os.path.split(shortPath)
    if head:
        pathOfHead = Path(head)
        if len(pathOfHead.parts) > 1:
            if pathOfHead.parts[1] == "lib":
                if "css" in tail:
                    return Response(requests.get('https://lib.pavlovia.org/'+tail).content,mimetype='text/css')
                return Response(requests.get('https://lib.pavlovia.org/'+tail).content,mimetype='text/javascript')
    if head:
        for path in lines:
            head2, tail2 = os.path.split(path)
            tailList.append(tail2)
            baseOfHead =         Path(head).parts[0]
            if tail2 ==   baseOfHead :
                if not tail: 
                    tail = "index.html"
                    html = Path(head2+'\\'+head+'\\'+tail.strip()).read_text()
                    soup = Soup(html)
                    liveJSScript = soup.new_tag('script')
                    with open(resource_path.joinpath('modified_live.js'), 'r') as file:
                      liveJSScript.string  = file.read()
                    soup.head.append(liveJSScript)
                    return str(soup)          
                return send_from_directory(head2+'\\'+head,tail.strip())   
    return "Please use 127.0.0.1:5000/add/EXPERIMENTPATH to start an experiment"

if __name__ == '__main__':
    app.run(debug=True)
