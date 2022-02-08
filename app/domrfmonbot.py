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
print(api_token)


def bot_message(botname, message):
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token),
                 params=dict(chat_id=botname, text=str(member) + message))


def ssl_expiry_datetime(host, port):
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


def knock_function(member, count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((str(member[0]), int(member[1])))
        if result == 0:
            sock.close()
            count = 0
            return('online')
        else:
            sock.close()
            count = count + 1
            if count == 5:
                bot_message(chat_name, str(member[2]) + ' Offline')
                count = 0
                return ('offline')
            knock_function(member, count)
    except Exception:
        sock.close()
        if count == 5:
            count = 0
            return ('offline')
        count = count + 1
        knock_function(member, count)


while 1 == 1:
    with open('config/ports.cfg', 'r') as f:
        ListAll = [line.rstrip('\n').split(';') for line in f]
        f.close()
    print(ListAll)
    for member in ListAll:
        count = 0
        res1 = knock_function(member, count)
        if res1 == 'offline':
            print("result of test: " + str(res1))
            bot_message(chat_name, str(member[2]) + ' offline')
        else:
            print('result of test: ' + str(res1))

    with open('config/hosts.cfg', 'r') as f:
        addres_list = f.read().splitlines()
        f.close()

    for member in addres_list:
        remains = ssl_expiry_datetime(member, 443)
        if remains != '0':
            if int(str((remains-datetime.datetime.now()).days)) < 30:
                bot_message(chat_name, str(member) + ' истекает сертификат!')
                good_list.append([member, (remains - datetime.datetime.now()).days])
        else:
            bad_list.append(member)
            bot_message(chat_name, str(member) + ' НЕДОСТУПЕН!')
 #    print(good_port_list)
 #    print(bad_port_list)
    time.sleep(300)
