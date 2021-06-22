from django.shortcuts import render
from .models import Positions, Candidates, Voters, Admin, Record
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import io, random
import requests

OTP=0

def getimage(request):

    def setPlt():
        pos = request.GET.get('position')
        count = Record.objects.filter(vote_posn=pos).count()
        names = Candidates.objects.filter(candid_posn= pos)
        l=[]
        v=[]
        print(count)
        if count:
            for i in names:
                l.append(i.candid_name)
                print(i.votes)
                v.append((i.votes/count)*100)

            objects = tuple(l)
            y_pos = np.arange(len(objects))
            performance = v

            plt.barh(y_pos, performance, align='center', alpha=0.5)
            plt.yticks(y_pos, objects)
            plt.ylabel('-------------candidates------------->>>')
            plt.xlabel('---------------vote %--------------->>>')
            plt.title('Percentage of votes obtained: ' + pos)

    def pltToSvg():
        buf = io.BytesIO()
        plt.savefig(buf, format='svg', bbox_inches='tight')
        s = buf.getvalue()
        buf.close()
        return s

    setPlt()  # create the plot
    if not Record.objects.filter(vote_posn= request.GET.get('position')).count():
        return HttpResponse('<h1> The votes for this position has not been casted yet! <br> Please Check after Sometime </h1>')
    else:
        print('mai bhi hoon na')
        svg = pltToSvg()  # convert plot to SVG
        plt.cla()  # clean up plt so it can be re-used
        response = HttpResponse(svg, content_type='image/svg+xml')
        return response

# Create your views here.
def login_register(request):
    if 'username' in request.COOKIES:
        name = request.COOKIES['username']
    return render(request,'polls/index.html')

def index(request):
    return render(request, 'polls/nav.html')


def candidates(request):
    valnew = []
    val_list = list(Positions.objects.filter().values('positn_name'))
    for i in val_list:
        l=list(i.values())
        valnew = valnew + l
    val_list = valnew[:]
    return render(request, 'polls/candidates.html', {'data': val_list})

def validate(request):
    pos = request.GET.get('position')
    name = request.GET.get('name')
    if Candidates.objects.filter(candid_posn= pos).count()>=10:
        b=0
        valnew=[]

    else:
        Candidates(candid_name = name, candid_posn = pos).save()
        valnew = []
        val_list = list(Candidates.objects.filter(candid_posn= pos).values('candid_name', 'candid_posn'))
        for i in val_list:
            l = list(i.values())
            valnew = valnew + l
        b=1
    data= { 'values': valnew, 'Bool': b}
    return JsonResponse(data)

def positions(request):
    valnew = []
    val_list = list(Positions.objects.filter())
    for i in val_list:
        valnew.append(i.positn_name)
    val_list = valnew[:]
    return render(request, 'polls/positions.html', {'data': val_list})

def addpos(request):
    val = request.GET.get('position')
    Positions(positn_name= val).save()
    valnew = []
    val_list = list(Positions.objects.filter())
    for i in val_list:
       valnew.append(i.positn_name)
    data = {'values': valnew}
    return JsonResponse(data)

def save(request):
    name = request.GET.get('name')
    passwd = request.GET.get('pass')
    number = request.GET.get('num')
    if not Voters.objects.filter(voter_num=number).exists():
        secret_code = str(random.randrange(100,300))+ name[:3]+'V'
        Voters(voter_name= name, voter_id= secret_code, voter_passwd= passwd, voter_num = number).save()
        data={'code': secret_code, 'bool': 1}
        print(data['code'])
    else:
        data={'bool': 0}
    return JsonResponse(data)

def v_login(request):
    res = "Not Feasible return to login page <a href='/login/'> login here</a>"
    global OTP
    if request.POST.get('vusername',0):
        if Voters.objects.filter(voter_id =request.POST['vusername'], voter_passwd =request.POST['vpassword']).exists() and request.POST['OTP']== OTP:
            request.session['voter_name'] = request.POST['vusername']
            return render(request, 'polls/voters.html')
        else:
            return HttpResponse(res)
    elif request.session['voter_name']:
        return render(request, 'polls/voters.html')
    else:
        return HttpResponse(res)

def a_login(request):
    res = "Not Feasible return to login page <a href='/login/'> login</a>"
    if request.POST.get('ausername', 0):
        if Admin.objects.filter(admin_name=request.POST['ausername'], admin_passwd=request.POST['apassword']).exists():
            request.session['admin_name']= request.POST['ausername']
            return render(request, 'polls/admin.html')
        else:
            return HttpResponse(res)
    elif request.session['admin_name']:
        return render(request, 'polls/admin.html')
    else:
        return HttpResponse(res)


def v_logout(request):
    res = "<script> location.href = '/' </script>"
    try:
        del request.session['voter_name']
    except KeyError:
        pass
    return HttpResponse(res)

def a_logout(request):
    res = "<script> location.href = '/' </script>"
    try:
        del request.session['admin_name']
    except KeyError:
        pass
    return HttpResponse(res)

def show(request):
    pos = request.GET.get('position')
    valnew = []
    val_list = list(Candidates.objects.filter(candid_posn= pos).values('candid_name'))
    print(val_list)
    for i in val_list:
        l = list(i.values())
        valnew = valnew + l
    data = {'values': valnew}
    return JsonResponse(data)

def current(request):
    valnew = []
    val_list = list(Positions.objects.filter())
    for i in val_list:
        valnew.append(i.positn_name)
    val_list = valnew[:]
    return render(request, 'polls/currents.html', {'data': val_list})

def vote(request):
    name = request.GET.get('candidate')
    voter= request.GET.get('name')
    pos = request.GET.get('position')
    if Voters.objects.filter(voter_id = voter,voter_permit = "yes").exists():
        if( not Record.objects.filter(voter_name= voter, vote_posn= pos).exists() ):
            valnew = []
            val_list = list(Candidates.objects.filter(candid_name= name).values('votes').distinct())
            print( name, voter, pos ,val_list)
            for i in val_list:
                l = list(i.values())
                valnew = valnew + l
            print(valnew[0])
            valnew[0]=valnew[0]+1
            Candidates.objects.filter(candid_name= name).update(votes= valnew[0])
            Record(voter_name=  voter, vote_posn= pos).save()
            data = {'name': name, 'Bool': 1}

        else:
            data= {'name': name, 'Bool': 0}

    else :
        data ={'name': name, 'Bool': 2}


    return JsonResponse(data)

def otp(request):
    id = request.GET.get('id')
    passwd = request.GET.get('pass')
    if Voters.objects.filter(voter_id= id, voter_passwd= passwd).exists():
        num=Voters.objects.filter(voter_id= id, voter_passwd= passwd).values('voter_num').distinct()

        url = "https://www.fast2sms.com/dev/bulk"
        array = ['xKw', 'BjY', 'OpI', 'WqP', 'AhQ']
        code = str(random.randrange(100,999))+random.choice(array)+str(random.randrange(1000,9999))

        querystring = {"authorization": "QKCX8k1MzLjm7yd5oAelYi9JbfcpTPWG6rgN4DB2HFxOt0wnvIJXqwZ4PIAdy02TBLRuQDpasemVKz5l", "sender_id": "FSTSMS", "language": "english", "route": "qt",
                       "numbers": "8959575687", "message": "8748",
                       "variables": "{BB}", "variables_values": code}

        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        global OTP
        OTP = code
        data={'Bool': 1}

    else:
        data= {'Bool' : 0}
    return JsonResponse(data)

def profile(request):
    valnew = []
    val_list = list(Voters.objects.filter(voter_id= request.session["voter_name"]))
    for i in val_list:
        valnew.extend([i.voter_name, i.voter_passwd, i.voter_num])
    val_list = valnew[:]
    return render(request,'polls/profile.html',{"info": val_list})

def cdelete(request):
    valnew = []
    name = request.GET.get('name')
    posn = request.GET.get('position')
    Candidates.objects.filter(candid_name=name, candid_posn= posn ).delete()
    val_list = list(Candidates.objects.filter(candid_posn=posn).values('candid_name', 'candid_posn').distinct())
    for i in val_list:
        l = list(i.values())
        valnew = valnew + l
    data ={'values': valnew}
    return JsonResponse(data)

def pdelete(request):
    valnew = []
    posn = request.GET.get('position')
    Positions.objects.filter( positn_name= posn ).delete()
    Candidates.objects.filter( candid_posn= posn ).delete()
    Record.objects.filter( vote_posn = posn ).delete()
    val_list = list(Positions.objects.filter().distinct())
    for i in val_list:
        valnew.append(i.positn_name)
    data = {'values': valnew}
    return JsonResponse(data)

def image(request):
    valnew = []
    val_list = list(Positions.objects.filter())
    for i in val_list:
        valnew.append(i.positn_name)
    val_list = valnew[:]
    return render(request,'polls/image.html', {'data': val_list})