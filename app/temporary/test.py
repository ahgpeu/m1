import requests
import ssl
import socket
import time
import datetime
good_list = []
bad_list = []
ListOff = {}
ListAll = ['ya.ru', 'yandex.ru', 'rbc.ru']

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
        print(member[0])
        print(member[1])
        print(member[2])
#стучимся в порт RDP, если закрыт или машины не существует, добавляем тачку, имя, место в списко ListOff
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((str(member[0]), int(member[1])))
            if result == 0:
                True
                print(str(member[2]) + ' ONLINE')
            else:
                print(str(member[2]) + ' OFFLINE')
            sock.close()
        except Exception:
            print(str(member[2]) + ' OFFLINE')

with open('config/ports.cfg', 'r') as f:
    ListAll = [line.rstrip('\n').split(';') for line in f]
    f.close()

knock_function(ListAll)

while 1 == 1:
    with open('config/hosts.cfg', 'r') as f:
        addres_list = f.read().splitlines()
        f.close()
    api_token = '5221567594:AAEnfrtksxLAMwdS0xvQmdWMDUDrGbxhiJc'

    for member in addres_list:
        remains = ssl_expiry_datetime(member)
        if remains != '0':
            if int(str((remains-datetime.datetime.now()).days)) < 30:
                requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token), params=dict(chat_id='@domrfmonitor', text= str(member) + ' истекает сертификат!'))
            good_list.append([member, (remains - datetime.datetime.now()).days])
        else:
            bad_list.append(member)
            requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token), params=dict(chat_id='@domrfmonitor', text= str(member) + ' НЕДОСТУПЕН!'))
    time.sleep(300)

