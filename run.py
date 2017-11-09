#!/usr/bin/python
#coding:utf-8

from app import app
from flask_cors import CORS

#允许跨域访问
CORS(app, resources=r'/*')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=14320,debug=True)
