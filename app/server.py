#!/usr/bin/python
#coding:utf-8

from flask import render_template,request,redirect,session, Response
from . import app
from config import *
from utils import login_request
from utils import json_encoder
import json
import db
from utils import is_exist
from utils import diff_keys

app.config.from_object(Table)
fields_cabinet=app.config.get('FIELDS_CABINET')  
fields_server=app.config.get('FIELDS_SERVER')
fields_server_show = app.config.get('FIELDS_SERVER_SHOW')
fields_idc = app.config.get('FIELDS_IDC')
POST_STANDARD_KEYS = ['idc_name', 'hostname', 'os', 'brand', 'model', 'cpu_num', 'cpu_model', 'memory', 'disk_info',
                      'total_disk', 'network_num', 'network_model', 'sys_kernel_version', 'sn_num', 'ip_address',
                      'isVirtual', 'update_time']

@app.route('/server/')
@login_request.login_request
def server():
    role = session.get('role')
    servers = db.list('server',fields_server_show)
    if servers:
        for i in servers:
            if i['cabinet_id']:
                cabinet = db.list('cabinet',fields_cabinet,i['cabinet_id'])
                if cabinet:
                    i['cabinet_id'] = cabinet['name']
                else:
                    return json.loads(
                        {"code": "1", "status": "failed", "result": "server: %s not get relatively cabinet."} % (
                        i['hostname']))
            else:i['cabinet_id'] = 'Unknown'
    return render_template("/server/serverlist.html",servers = servers,role = role)

@app.route("/serveradd/",methods=['GET','POST'])
@login_request.login_request
def serveradd():
    if request.method == 'GET':
	return render_template('/server/serveradd.html',info = session,role = session.get('role'))
    if request.method == 'POST':
	data = dict((k,v[0]) for k,v in dict(request.form).items())
	l = []

	for i in db.list('server',fields_server):
	    l.append(i['hostname'])
	if not data['hostname']:
	    return json.dumps({'code':1,'errmsg':'hostname can not be null'})
	elif data['hostname'] not in l:
	    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
	    db.add('server',conditions)
	    return json.dumps({'code':0,'result':'add server success'})
	return json.dumps({'code':1,'errmsg':'server name is exist'})


#增加主机api接口
@app.route("/api/v1/serveradd/",methods=['POST'])
def serveraddapi():
    if request.method == 'POST':
        try:
            data = request.get_data()
            postData = json.loads(data)
        except Exception as e:
            return json.dumps({"code": "1","status": "failed","result": "Data type must be json."})
        postKeys = postData.keys()
        diff_key = diff_keys.diff_keys(postKeys,POST_STANDARD_KEYS)
        return_str = "Unknow key: %s!" % (str(diff_key))
        if diff_key:return json.dumps({"code": "1","status": "failed","result": return_str})
        if not is_exist.is_exist_idc(postData["idc_name"], fields_idc): return json.dumps({"code": "1","status": "failed","result": "Idc not exist!"})
        if is_exist.is_exist_ip(postData["ip_address"], fields_server):
            server_id = is_exist.is_exist_ip(postData["ip_address"], fields_server)
            conditions = [ "%s='%s'" %  (k,v) for k,v in postData.items()]
            db.update('server',conditions,server_id)
            return json.dumps({"code": "0", "status": "success", "result": "Update server success!"})
        else:
            try:
                conditions = [ "%s='%s'" %  (k,v) for k,v in postData.items()]
                db.add('server', conditions)
                return json.dumps({"code": "0","status": "success","result": "Add server success!"})
            except Exception as e:
                return json.dumps({"code": "1","status": "failed","result": "add db failed."})
    if request.method == 'GET':
        return json.dumps({"code": "1","status": "failed","result": "Get method not allow."})

#根据主机id获取主机详情
@app.route('/api/v1/serverinfo/')
# @login_request.login_request
def serverinfo():
    id = request.args.get('id')
    server = db.list('server',fields_server,id)
    if server:
        # print server['update_time']
        # server['update_time'] = server['update_time'].strftime('%Y-%m-%d %H:%M:%S')
        rt = json.dumps({"code": "0", "status": "success", "result": server}, cls=json_encoder.JsonEncoder)
        response = Response(rt, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        # return json.dumps({"code": "0", "status": "success", "result": server}, cls=json_encoder.JsonEncoder)
        return response
    else: return json.dumps({"code": "1", "status": "failed", "result": "Get server info failed"})


#根据主机id获取主机详情
@app.route('/api/v1/serverupdate/<id>',methods=['POST'])
# @login_request.login_request
def serverupdate(id):
    if request.method == 'POST':
        #判断是否为json串
        try:
            data = request.get_data()
            postData = json.loads(data)
        except Exception as e:
            return json.dumps({"code": "1","status": "failed","result": "Data type must be json."})
        #检查传入keys
        postKeys = postData.keys()
        diff_key = diff_keys.diff_keys(postKeys, fields_server)
        return_str = "Unknow key: %s!" % (str(diff_key))
        if diff_key: return json.dumps({"code": "1", "status": "failed", "result": return_str})
        #进行更新 操作
        try:
            conditions = ["%s='%s'" % (k, v) for k, v in postData.items()]
            db.update('server', conditions, id)
            response = Response(json.dumps({"code": "0","status": "success","result": "Update server success."}), mimetype='application/json')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Exception as e:
            return json.dumps({"code": "1","status": "failed","result": "Update server failed."})

@app.route('/server_update_msg/')
@login_request.login_request
def server_update_msg():
    id = request.args.get('id')
    server = db.list('server',fields_server,id)
    return json.dumps({'code':0,'result':server})

@app.route('/server_update/',methods=['GET','POST'])
@login_request.login_request
def server_update():
    data = dict((k,v[0]) for k,v in dict(request.form).items())
    conditions = [ "%s='%s'" %  (k,v) for k,v in data.items()]
    db.update('server',conditions,data['id'])
    return json.dumps({'code':0,'result':'update completed!'})

@app.route('/server_delete/',methods=['POST'])
@login_request.login_request
def server_delete():
    id = request.form.get('id')
    db.delete('server',id)
    return json.dumps({'code':0,'result':'delete success!'})

@app.route('/serverdetail/')
@login_request.login_request
def serverdetail():
    role = session.get('role')
    servers = db.list('server',fields_server)
    if servers:
        for i in servers:
            cabinet = db.list('cabinet',fields_cabinet,i['cabinet_id'])
            if cabinet:
                i['cabinet_id'] = cabinet['name']
            else:
                continue
    return render_template("/server/serverdetail.html",servers = servers,role = role)