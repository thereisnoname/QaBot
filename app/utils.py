import json
import socket
import logging

from django.shortcuts import HttpResponse
from QaBot.settings import QASNAKE_HOST, QASNAKE_PORT
from app.models import *

logger = logging.getLogger("django")

# 服务工具包 Utils
#   Aux functions for views.py
#


# Section A 数据库实体管理 Entity
def update_userlist(users):
    User.update_userlist(users)
    # u, created = User.objects.get_or_create(uid=users['uid'], nickname=users['nickname'], gender=users['gender'])

def update_questionlist(ques):
    q = Question.update_questionlist(ques)
    return q

def update_answerlist(ans):
    Answer.update_answerlist(ans)


def qa_snake(kw):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((QASNAKE_HOST, QASNAKE_PORT))
        client.settimeout(30)
        client.send(kw.encode('utf8'))
        ans = client.recv(4096).decode('utf8')
        logger.info('[QA-Snake] %s...' % ans[:30])
        return ans
    except:
        return None


# Section B 语法糖 Wrapper
def response_write(jsonData):
    response = HttpResponse(json.dumps(jsonData, ensure_ascii=False))
    return response


def json_load(byteData):
    try:
        strData = isinstance(byteData, bytes) and byteData.decode('utf8') or byteData
        jsonData = json.loads(strData, encoding='utf8', parse_int=int, parse_float=float)
        logger.info('Received Json Data: %s' % jsonData)
        return jsonData
    except :
        raise
        return None



# Section C 错误码 Error Code
def die(codeno):
    ERRMSG = {
        200: 'Done',
        400: 'Malformatted Request',
        401: 'Not Authorized',
        403: 'Missing Parameter or TypeError',
        404: 'Resource Not Found',
        405: 'Method Not Allowed',
        500: 'Server Internal Error',
    }

    return {'errorno': codeno, 'errormsg': ERRMSG.get(codeno) or 'Unkown Error'}


# Section D 默认值配置 Defaults
