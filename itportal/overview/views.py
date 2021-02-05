from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from overview.models import host_notmonitor, UserExpire


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
    res_tempuser = list(UserExpire.objects.all().values
                        ('userid', 'username', 'company', 'phone', 'email',
                         'state', 'expiretime', 'manager')
                        )
    return JsonResponse(res_tempuser, safe=False)
