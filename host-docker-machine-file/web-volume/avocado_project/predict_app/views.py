from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import predict
from . import models
from . import forms

from datetime import datetime
import threading
import json
# Create your views here.


def form(request, message="분석할 데이터 제출"):

    avocadousers = list(str(u.email) for u in models.AvocadoUser.objects.all())

    form = forms.FileUploadHistoryForm()

    context = {'message':message,
               'avocadousers':avocadousers,
               'form':form
               }
    return render(request, 'predict_app/form.html',context=context)



def upload(request):

    form = forms.FileUploadHistoryForm(request.POST, request.FILES)


    if form.is_valid():

        task = form.save()
        context = {"task": task}

        #thread = threading.Thread(target=predict.LearningModuleRunner, args=(task, 30))
        #thread.start()

        return render(request, 'predict_app/success.html', context=context)
    else :
        avocadousers = list(str(u.email) for u in models.AvocadoUser.objects.all())

        context = {'message': "제출 형식에 오류가 있습니다.",
                   "avocadousers": avocadousers,
                   'form':form }
        return render(request, 'predict_app/form.html', context=context)# HttpResponse(form.errors)



    '''
    user = request.POST['user']
    data = request.POST['data']
    weather = request.POST['weather']
    timestep = request.POST['timestep']

    print(type(data))
    print(data)
    newstring = ""
    for d in data :
        newd = str(d).replace("\'","\"")
        newstring = newstring+newd

    data = newstring

    try:
        if set(json.loads(data).keys()) == set(['Data','Date']):
            task = models.Task(
                user=models.AvocadoUser.objects.get(email=user),
                data=data,
                weather=weather,
                timestep=timestep
            )
            task.save()




            thread = threading.Thread(target=predict.LearningModuleRunner, args=(task, 30))
            thread.start()

            context = {"task" : task}

            return render(request, 'predict_app/success.html', context=context)

        else:
            return redirect('form')
    except json.decoder.JSONDecodeError as e:
        return redirect('form')
    '''

def shownow(request):

    top_eight = ['롯데알미늄(진천공장)',
     '한일제관(주)-대전공장',
     '깨끗한나라 주식회사',
     '(주)농심-포승배송지점(물류)',
     '한국제지(주)',
     '대한제분(주)(인천공장)',
     '(주)오뚜기-대풍공장',
     '오뚜기라면(주)',]



    context = {}

    return render(request, 'predict_app/shownow.html', context=context)


def showpredict(request):
    context = {}
    return render(request, 'predict_app/showpredict.html', context=context)

def company(request, page_number=1):

    items = 50
    next_page = str(int(page_number) + 1)
    prev_page = str(int(page_number) - 1)

    if request.method =="POST":

        search = str(request.POST['search'])

        all_company= models.Company.objects.filter(name__contains=search)

    else :

        total_company = int(models.Company.objects.count())
        all_company = models.Company.objects.all()[items*(int(page_number)-1):items*int(page_number)]



    context={'all_company':all_company,
             'page_number': page_number,
             'next_page': next_page,
             'prev_page':prev_page}

    return render(request, 'predict_app/company.html', context=context)


def company_info(request, company_id=1):
    company_id = int(company_id)

    company =  models.Company.objects.get(id=company_id)

    pallet_datas = models.PalletData.objects.filter(company=company)

    for_graph = []
    for pada in pallet_datas:
        ts = str(pada.date)[:10].split("-")
        for_graph.append([ ts[0],ts[1],ts[2], str(pada.pallet_out) ])

    for_graph.append([ts[0], ts[1], str(int(ts[2])+15), '0'])
    for_graph.append(["2017","11","1","0"])


    for_graph = sorted(for_graph)

    context={
        'company':company,
        'pallet_datas':pallet_datas,
        'for_graph':for_graph,
             }

    return render(request, 'predict_app/company_info.html', context=context)


    '''
    task = models.FileUploadHistory.objects.get(id=task_id)

    result = json.loads(task.result)

    if list(result.keys())==['result']:
        is_finished = 0
        chartdata = None
    else :
        is_finished = 1

        time = result["Date"]
        data = result["Data"]
        #data = result[:-30]
        #predict = result[-30:]

        chartdata = "["

        #remain = len(time)
        index = 0
        for t in time :
            ts = t.split("-")
            if len(time) - index > 30 :
            #if remain > 30  :
                #chartdata.append([t,data[index], 0])
                chartdata += "[ new Date(" + ts[0] + "," + ts[1]+ "," + ts[2] + "),"+str(data[index])+",0], "
            else :
                #chartdata.append([t,0,data[index]])
                chartdata += "[ new Date(" + ts[0] + "," + ts[1]+ "," + ts[2] + "),0,"+str(data[index])+"],"
            #remain -= 1
            index += 1
        chartdata +="]"

    context = {"task":task,
               "is_finished":is_finished,
               "chartdata":chartdata
               }
               
    '''


