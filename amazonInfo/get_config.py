import json
import os


def read_file_json():
    f = open(os.path.abspath('config.json'))  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    text = line.strip('\n').replace(" ", "")
    while line:
        # line# print(line, end='')  # 在 Python 3中使用# 后面跟 ',' 将忽略换行符
        line = f.readline().strip('\n').replace(" ", "")
        text += line

    f.close()  # 获取文件夹大小自己用list(os.walk(path))解决
    return text


def get_json_text():
    json_text = read_file_json()
    text = eval(json_text)
    json_str = json.dumps(text)
    data = json.loads(json_str)
    return data


def get_eamilFromName():
    return get_json_text()['eamilFromName']


def get_emailToName():
    return get_json_text()['emailToName']


def get_emailTo():
    return get_json_text()['emailTo']


def get_emailSubject():
    return get_json_text()['emailSubject']


def get_emailBody():
    return get_json_text()['emailBody']


def get_smtpServer():
    return get_json_text()['smtpServer']


def get_emailFromSend():
    return get_json_text()['emailFromSend']


def get_emailPassword():
    return get_json_text()['emailPassword']


def get_emailToCcName():
    return get_json_text()['emailToCcName']


def get_emailCc():
    print('---' + str(get_json_text()['emailCc']))
    return get_json_text()['emailCc']
