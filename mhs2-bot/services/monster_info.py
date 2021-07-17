import json
from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/VenseChang/mhs2/master/data/data.json'
datas = json.loads(urlopen(url).read())

def monster_names(text):
    return list(filter(lambda name: text in name , datas.keys()))

def monster_name(data):
    names = filter(lambda x: x, 
                   [data['zh-hant'],
                    data['en']])
    return ' / '.join(names)

def monster_info(field, data):
    if field == 'name':
        return monster_name(data[field])
    elif field == 'egg':
        return 'O' if data[field] or False else 'X'
    else:
        return data[field]

def translation(key):
    mapping = {
        'no': 'No. ',
        'name': '名稱： ',
        'egg': '可孵蛋？  ',
        'normal': '普通狀態： ',
        'angry': '生氣狀態： ',
        'nest': '歸巢加成： ',
        'weakness': '弱點屬性： ',
        'head': '・ 頭： ',
        'feet': '・ 腳： ',
        'body': '・ 身體： ',
        'wing': '・ 翅膀： ',
        'abdomen': '・ 腹部： ',
        'tail': '・ 尾巴： '
    }
    return mapping[key]

def render_info(text, mode, output = ''):
    monsters = monster_names(text)
    if mode == 'precise':
        monsters = list(filter(lambda name: name[-len(text):] == text, monsters))

    for monster in monsters:
        data = datas[monster]
        for key in ['no', 'name', 'egg', 'normal', 'angry', 'nest', 'weakness']:
            if key in data:
                output += "{}{}\n".format(translation(key), monster_info(key, data))
        if len(data['parts']) > 0:
            output += "部位破壞：\n"
            for key in ['head', 'feet', 'body', 'wing', 'abdomen', 'tail']:
                if key in data['parts']:
                    output += "{}{}\n".format(translation(key), data['parts'][key])
        if len(monsters) > 1:
            output += "\n"
    return output or "您輸入的關鍵字找不到對應的魔物"