with open('config/ports.cfg', 'r') as f:
    addres_list = [line.rstrip('\n').split(';') for line in f]
    f.close()
print(addres_list)
