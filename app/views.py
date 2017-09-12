from django.shortcuts import redirect, render, resolve_url
from django.views.decorators.csrf import csrf_exempt
from QaBot.settings import LOG_FILE
from app.utils import *
from app.scheds import *

# 业务逻辑+视图层 Service/Controller + View
#   合理抽象出工具utils.py:)
#


# Headless API Views
@csrf_exempt
def user(request):
    if request.method == 'POST':
        data = json_load(request.body)
        if not data:
            return response_write(die(400))
        print('Got users: %s' % data)

        data_all = data['users']
        for data in data_all:
            id = data.get('id') or -1
            nickname = data.get('nickname') or ''
            gender = data.get('gender') or 0

            u = {
                'uid' : id,
                'nickname' : nickname,
                'gender' : gender
            }

            update_userlist(u)
        return  response_write(die(200))
    return HttpResponse("The request should be POST")


@csrf_exempt
def q(request):
    if request.method == 'POST':
        data = json_load(request.body)
        if not data:
            return response_write(die(400))

        uid = data.get('uid') or -1
        question = data.get('question') or ''
        print('Get <%s>: %s' % (uid, question))

        q = {
            'uid' : uid,
            'question' : question,
        }
        qid = update_questionlist(q).qid

        ans = Answer.objects.filter(question = qid)
        if ans.exists():
            data = {
                'answer': ans[0].content,
                'qid': qid,
            }
        else:
            data = {
                'helpers': ['@dsfsd6s46SDVD', '@DVS68d4DVSvsDVSv4654v6s8'],
                'qid': qid,
            }
        return response_write(data)


@csrf_exempt
def a(request):
    if request.method == 'POST':
        data = json_load(request.body)
        if not data:
            return response_write(die(400))

        uid = data.get('uid') or -1
        qid = data.get('qid') or ''
        answer = data.get('answer') or ''
        print('Get <%s>-[%d]: %s' % (uid, qid, answer))

        if not Question.objects.filter(qid = qid).exists():
            return response_write({'info':'The Question you post is not exist!'})

        a = {
            'uid' : uid,
            'qid' : qid,
            'answer' : answer
        }

        update_answerlist(a)

        return response_write({'info': 'OK'})


# Browser-oriented Views
@csrf_exempt
def index(request):
    if request.method == 'POST':
        kw = request.POST.get('kw')
        if kw:
            ans = '暂时没设计好:('    # NOT urgent TODO: dispatch?
            return render(request, 'index.html', {'ans': ans})
    return render(request, 'index.html')


@csrf_exempt
def log(request):
    if request.GET.get("do") == 'clean':
        try:
            f = open(LOG_FILE, 'w+')
            f.write('===== [Log Cleaned] =====\n')
            f.close()
        except IOError as ioe:
            return HttpResponse('Failed due to %s... :(' % ioe)
        return redirect(resolve_url(log))
    else:
        f = open(LOG_FILE)
        logs = [l for l in f.readlines()]
        logs = logs[:100]
        return render(request, 'log.html', {'logs': logs})
