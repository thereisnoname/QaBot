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
    # if request.method == 'POST':
    if True:
        data = json_load(request.body)      # TODO: what json format
        if not (data and data.get('question')):
            if data and data.get('uid'):
                data={
                    'answer':'where the fuck question is?',
                    'qid':data.get('uid'),
                }
                return response_write(data)
            return response_write({'ans':'where the fuck question is?'})
        uid = data.get('uid') or '-1'
        question = data.get('question') or ''
        print('Get <%s>: %s' % (uid, question))
        ans = qa_snake(question)
        q = {
            'uid' : uid,
            'keywords' : ans['kw'],
            'question' : question,
        }
        similar_qid=find_alike(q)
        if similar_qid:
            #find the ans to this qid
            #then return it!
            # or maybe save the qid in the value qid
            #the return qid is not the similar qid!!
            ans = qid_get_ans_con(similar_qid)
            data = {
                'answer' : ans,
                'qid' : similar_qid,
                # so what is qid now??
            }
            return response_write(data)
            #quchifan,denghuihuilaixie
        else:
            qid = update_questionlist(q).qid
            a = {
                'uid': 'QaBot',
                'qid': qid,
                'answer': ans['ans']
            }
            update_answerlist(a)

        ans = Answer.objects.filter(question = qid)
        if ans.exists():
            for final_ans in ans:
                if final_ans:
                    if final_ans.content:
                        data = {
                            'answer': ans[0].content,
                            'qid': qid,
                        }
                        return response_write(data)
        data = {
                #what's this??
            'helpers': ['@dsfsd6s46SDVD', '@DVS68d4DVSvsDVSv4654v6s8'],
            'qid': qid,
        }
        return response_write(data)



@csrf_exempt
def a(request):
    print("in a")
    if request.method == 'POST':
        print("in a")
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
   # return response_write({'info': 'NOT POST?'})



# Browser-oriented Views
@csrf_exempt
def index(request):
    if request.method == 'POST':
        kw = request.POST.get('kw')
        if kw:
            re = qa_snake(kw)    # NOT urgent TODO: dispatch?
            q = {
                'uid': 1,
                'keywords': re['kw'],
                'question': kw,
            }
            similar_qid = find_alike(q)
            if similar_qid:
                # in index, we just return the ans
                # and now we got qid to the ans
                #do nothing
                qid = similar_qid
                pass
            else:
                print ("\n key is "+q['keywords'])
                qid = update_questionlist(q).qid
                data = {
                    'uid':1,
                    'qid':qid,
                    'answer':re['ans'],
                }
                update_answerlist(data)
            ans = Answer.objects.filter(question=qid)
            for final_ans in ans :
                if final_ans:
                    if final_ans.content:
                        return render(request, 'index.html', {'ans': final_ans.content})
            return render(request,'index.html',{'ans':'no such ans in qasnake'+'\t'+'key words is '+kw})
    return render(request, 'index.html',{'ans':'no such keyword'})


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
