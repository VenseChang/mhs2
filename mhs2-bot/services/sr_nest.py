import json
from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/VenseChang/mhs2/master/data/nest_info/sr-nest-data.json'
datas = json.loads(urlopen(url).read())

def nests():
    return list(datas['nest'].keys())

def monsters():
    return list(datas['monsters'].keys())

def render_sr_info(text, sr_type, output = ''):
    target = text if sr_type == 'nest' else list(filter(lambda name: text == name, monsters()))[0]
    data = datas[sr_type][target]

    output += '{}：'.format(target)
    for d in data:
        output += '\n・ {}'.format(d)
    return output