#coding:utf-8
import app
import db


def  is_exist_ip(ip,fields):
    server_id = False
    # fields_server = app.config.get('FIELDS_SERVER')
    servers = db.list('server', fields)
    for server in servers:
        if server['ip_address'] == ip:server_id = server['id'];break
        else:continue
    return server_id


def is_exist_idc(idc_name, fields):
    flag = False
    # fields_idc = app.config.get('FIELDS_IDC')
    idc_name_up = idc_name.upper()
    idc_name_low = idc_name.lower()
    idcs_info = db.list('idc', fields)
    for idc_info in idcs_info:
        if idc_info['name'] == idc_name_low or idc_info['name'] == idc_name_up:flag = True;break
        else:continue
    return flag

def is_exist_v(sheet,field,value,fields):
    flag = False
    # fields_field = app.config.get(fields_name)
    res = db.list(sheet, fields)
    for re in res:
        if re[field] == value:flag = True;break
        else:continue
    return  flag


