oui_dict = {}

def oui_lookup(mac):
    return oui_dict.get(mac.upper())

with open('oui_list.txt','r') as textfile:
    for line in textfile:
        line = line.split()
        oui_dict[line[0]] = line[1]


