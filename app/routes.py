# -*- coding: utf-8 -*-
import time
import ssl
import socket
import datetime
from flask import render_template
from app import app
@app.route('/')
@app.route('/index')
def index():
    good_list = []
    bad_list = []
    good_port_list = []
    bad_port_list = []
    with open('app/config/hosts.cfg', 'r') as f:
        addres_list = f.read().splitlines()
        f.close()
    with open('app/config/ports.cfg', 'r') as f:
        ListAll = [line.rstrip('\n').split(';') for line in f]
        f.close()
    
    def ssl_expiry_datetime(host, port=443):
        ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host,)
    # 3 second timeout because Lambda has runtime limitations
        conn.settimeout(3.0)
        try:
            conn.connect((host, port))
            ssl_info = conn.getpeercert()
            res = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        except:
            res = '0'
        return res
    
    def knock_function(ListAll):
        for member in ListAll:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((str(member[0]), int(member[1])))
                if result == 0:
                    good_port_list.append(member[2])
                else:
                    bad_port_list.append(member[2])
                sock.close()
            except Exception:
                bad_port_list.append(member[2])
    
    knock_function(ListAll)
    for member in addres_list:
        remains = ssl_expiry_datetime(member)
        if remains != '0':
            good_list.append([member, (remains - datetime.datetime.now()).days])
        else:
            bad_list.append(member)


    timer = time.ctime()
    return render_template('index.html', good_list = good_list, bad_list = bad_list, good_port_list = good_port_list, bad_port_list = bad_port_list, timer = timer)
