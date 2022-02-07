import socket
import datetime
ListOff = {}

ListAll = ['collab-edge.domrfbank.ru', 'vcs1.domrfbank.ru', 'vcs2.domrfbank.ru']
for member in ListAll:
    if member != '':
#стучимся в порт RDP, если закрыт или машины не существует, добавляем тачку, имя, место в списко ListOff
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((str(member), 5061))
            if result == 0:
                True
                print(str(member) + ' ONLINE')
            else:
                print(str(member) + ' OFFLINE')
            sock.close()
        except Exception:
            print(str(member) + ' OFFLINE')
