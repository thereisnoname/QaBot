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
    if request.method == 'POST':    # TODO: call User.update_userlist()
        pass


@csrf_exempt
def q(request):
    if request.method == 'POST':
        data = json_load(request.body)      # TODO: what json format
        if data and data.get('kw'):
            ans = qa_snake(data.get('kw'))
            return response_write({'ans': ans})


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
