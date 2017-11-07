#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session
from . import app
from config import *
from utils import login_request
import json
import db

app.config.from_object(Table)
fields_netdevice=app.config.get('FIELDS_NETDEVICE')

@app.route('/netdevice/')
@login_request.login_request
def netdevice():
    print 'aaa'
    role = session.get('role')
    netdevices = db.list('netdevice',fields_netdevice)
    return render_template("/netdevice/netdevicelist.html",netdevices = netdevices,role = role)

@app.route('/netdevice_msg/')
@login_request.login_request
def netdevice_msg():
    netdevices = db.list('netdevice',fields_netdevice)
    return json.dumps({'result':netdevices})

@app.route("/netdeviceadd/",methods=['GET','POST'])
@login_request.login_request
def netdeviceadd():
    if request.method == 'GET':
	return render_template('/netdevice/netdeviceadd.html',info = session,role = session.get('role'))
    if request.method == 'POST':
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	l = []

	for i in db.list('netdevice',fields_netdevice):
	    l.append(i['name'])
	if not data['name']:
	    return json.dumps({'code':1,'errmsg':'name can not be null'})
	elif data['name'] not in l:
	    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	    db.add('netdevice',conditions)
	    return json.dumps({'code':0,'result':'add netdevice success'})
	return json.dumps({'code':1,'errmsg':'netdevice name is exist'})

@app.route('/netdevice_update_msg/')
@login_request.login_request
def netdevice_update_msg():
    id = request.args.get('id')
    netdevice = db.list('netdevice',fields_netdevice,id)
    return json.dumps({'code':0,'result':netdevice})

@app.route('/netdevice_update/',methods=['GET','POST'])
@login_request.login_request
def netdevice_update():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('netdevice',conditions,data['id'])
    return json.dumps({'code':0,'result':'update completed!'})

@app.route('/netdevice_delete/',methods=['POST'])
@login_request.login_request
def netdevice_delete():
    id = request.form.get('id')
    db.delete('netdevice',id)
    return json.dumps({'code':0,'result':'delete success!'})
