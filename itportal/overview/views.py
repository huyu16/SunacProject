from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from overview.models import host_notmonitor, UserExpire
from data.data_monitor import monitor_expireuser
import json


# from data import data_monitor
# import json
# from django.core.serializers import serialize

# Create your views here.


def index(request):
    return render(request, "overview/index.html")


def host_monitordata(request):
    # data_list = data_monitor.monitor_data()
    # return HttpResponse(json.dumps(data_list))
    # res = serialize('json', host_notmonitor.objects.all(), fields=('id','name'))
    res = list(host_notmonitor.objects.all().values('id', 'name', 'ip', 'owner', 'department'))
    return JsonResponse(res, safe=False)


def user_expire(request):
    t_expireuser = monitor_expireuser()
    l_tempuser = list(t_expireuser)
    return JsonResponse(l_tempuser, safe=False)


def savedata_manager(request):
    if request.is_ajax():
        data = json.loads(request.body)
        t_id = data['id']
        manangeruser = data['manageruser']
        UserExpire.objects.filter(id=t_id).update(manager=manangeruser)
    return HttpResponse(0)

