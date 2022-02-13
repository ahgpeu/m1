import requests
import ssl
import socket
import time
import datetime

chat_name = '@domrfmonitor'
good_list = []
bad_list = []
good_port_list = []
bad_port_list = []
with open('config/bot.cfg', 'r') as f:
    api_token = f.read().splitlines()[0]
    f.close()


def bot_message(botname, message):
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token),
                 params=dict(chat_id=botname, text=message))


def ssl_expiry_datetime(host, port):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host, )
    conn.settimeout(3.0)
    try:
        conn.connect((host, port))
        ssl_info = conn.getpeercert()
        res = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    except:
        res = '0'
    return res


def knock_function(member_knock):
    count1 = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    while count1 <= 5:
        try:
            result = sock.connect_ex((str(member_knock[0]), int(member_knock[1])))
            if result == 0:
                sock.close()
                return 'online'
            count1 += 1
            sock.close()
            time.sleep(3)
        except socket.error as error:
            count1 += 1
            time.sleep(3)
            sock.close()
    return 'offline'


while 1 == 1:
    with open('config/ports.cfg', 'r') as f:
        ListAll = [line.rstrip('\n').split(';') for line in f]
        f.close()
    for member in ListAll:
        res1 = knock_function(member)
        if res1 == 'offline':
            bad_port_list.append(member)
        else:
            good_port_list.append(member)

    with open('config/hosts.cfg', 'r') as f:
        addres_list = f.read().splitlines()
        f.close()

    for member in addres_list:
        remains = ssl_expiry_datetime(member, 443)
        if remains != '0':
            if int(str((remains - datetime.datetime.now()).days)) < 30:
                good_list.append([member, (remains - datetime.datetime.now()).days])
                bot_message(chat_name, str(member) + ' истекает сертификат!')
            else:
                good_list.append(member)
        else:
            bad_list.append(member)
            bot_message(chat_name, str(member) + ' НЕДОСТУПЕН!')
    if len(bad_list) > 0 or len(bad_port_list):
        for member in bad_list:
            bot_message(chat_name, str(member) + ' НЕДОСТУПЕН')
            bad_list = []
            print(str(member) + ' НЕДОСТУПЕН')
        for member in bad_port_list:
            bot_message(chat_name, str(member[2]) + ' offline')
            print(str(member[2]) + ' offline')
            bad_port_list = []
        time.sleep(300)
    time.sleep(5)
