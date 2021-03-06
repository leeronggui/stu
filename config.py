# coding:utf-8

class MysqlConfig():
    SQL_HOST='localhost'
    SQL_USER='root'
    SQL_PASSWD=''
    SQL_DB='reboot10'

class Table():
    FIELDS_USER=['id','name','name_cn','password','email','email_password','mobile','role','status']
    FIELDS_IDC=['id','name','name_cn','address','adminer','phone','num']
    FIELDS_CABINET=['id','name','idc_id','u_num','power']
    FIELDS_SERVER = ['id', 'idc_name', 'cabinet_id', 'location', 'hostname', 'os', 'brand', 'model', 'cpu_num',
                     'cpu_model', 'memory', 'disk_info',
                     'total_disk', 'network_num', 'network_model', 'sys_kernel_version', 'sn_num', 'ip_address',
                     'isVirtual', 'adminer', 'phone', 'update_time', 'comments']
    FIELDS_SERVER_SHOW = ['id', 'idc_name', 'cabinet_id', 'hostname', 'ip_address', 'model', 'cpu_num', 'memory',
                          'total_disk', 'isVirtual']
    FIELDS_CODE=['id','update_date','update_persion','project','message']
    FIELDS_OPS_JOBS=['id','apply_date','apply_type','apply_desc','deal_persion','status','deal_desc','deal_time','apply_persion']
    FIELDS_NETDEVICE = ['id', 'idc_name', 'cabinet_id', 'location', 'netdevice_name', 'brand', 'model', 'memory',
                        'ele_port', 'opt_port', 'sn_num', 'role', 'manage_ip', 'alternate_ip', 'adminer', 'phone',
                        'comments']
    FIELDS_NETDEVICE_SHOW = ['id', 'idc_name', 'cabinet_id', 'netdevice_name', 'manage_ip', 'brand', 'role', 'memory']

class RemoteHost():
    HOST1=['192.168.1.100',22,'root','123456']
    HOST2=['192.168.1.101',22,'root','123456']
    HOST3=['192.168.1.102',22,'root','123456']

class ProUrl():                                                             
    BASEURL='https://******************/svn/*******'
    URL={'cms':BASEURL+'cms','command':BASEURL+'command','common':BASEURL+'common','dist':BASEURL+'dist','doc':BASEURL+'doc','doctor':BASEURL+'doctor','ecg':BASEURL+'ecg','framework':BASEURL+'framework','requirements':BASEURL+'requirements','run':BASEURL+'run','web':BASEURL+'web','weixinapp':BASEURL+'weixinapp'}
