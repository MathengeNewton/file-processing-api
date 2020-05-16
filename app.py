from flask import Flask,request,jsonify
import os
import datetime
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['DEBUG']=True


def analitics(loadfile):
    mainfile = loadfile['body'][0]
    file = pd.read_json(mainfile)
    #clean out currency rows
    file['gross income'] = file['gross income'].str.replace('$','',regex = True).astype(float)
    file['salarie'] = file['salarie'].str.replace('$','',regex = True).astype(float)
    file['expenses'] = file['expenses'].str.replace('$','',regex = True).astype(float)
    #generate tax row
    file['Total Income'] = file['salarie'] + file['expenses']
    file['monthly tax'] = (file['gross income'] - file['Total Income'] ) * 0.1
    #jsonify return 
    finaldf = file.to_json(orient = 'split')
    return finaldf


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(405)
def method_not_allowed(e):
    return "<h1>405</h1><p>Method not allowed</p>", 404

@app.route('/data-center',methods = ['GET','POST'])
def main():
    somefile = request.data
    print(somefile)
    loadfile = somefile.get_json()   
    analyse = analitics(loadfile)    
    if (analyse):
        outcome = {
            'data':analyse
        }        
        return jsonify(outcome),201
    else:
        return page_not_found(404)
    
    
    
    
    

app.run()
