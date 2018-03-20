from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Max, Min, Count

from . import models


from .shortcuts.googlechart import trend_json, rank_json, order_rank_json, order_analysis_json
from .shortcuts.list import list_json

import json
# Create your views here.



# Clean backend API
# TODO : REST API 화 시키기


def chart_rhythm_api(request):
    if request.method=='POST':
        data = json.loads(request.body)
        m = str(data['m'])
        id = int(data['id'])
        filterd = data['filter']
    else :
        return JsonResponse({'error': 'not available method : GET'})

    if m=='code':
        M = models.Code
        row = M.objects.get(id=id)
        items = models.PalletCode.objects.all()
        pallets = models.KppPalletData.objects.filter(code=row)

    elif m=='palletcode' :
        M = models.PalletCode
        row = M.objects.get(id=id)
        items = models.Code.objects.all()
        pallets = models.KppPalletData.objects.filter(palletcode=row)

    else :
        pallets = models.KppPalletData.objects.all()
        items = models.PalletCode.objects.all()

    pallets = pallets.filter(date__year__gte=int(filterd['year__gte']),
                             date__year__lte=int(filterd['year__lte']),
                             )



    return JsonResponse(order_rank_json(pallets,m,items))

def chart_rhythm_plot_api(request):
    if request.method=='POST':
        data = json.loads(request.body)
        m = str(data['m'])
        id = int(data['id'])
        filterd = data['filter']
    else :
        return JsonResponse({'error': 'not available method : GET'})

    if m=='code':
        M = models.Code
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(code=row)

    elif m=='palletcode' :
        M = models.PalletCode
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(palletcode=row)

    else :
        pallets = models.KppPalletData.objects.all()

    pallets = pallets.filter(date__year__gte=int(filterd['year__gte']),
                             date__year__lte=int(filterd['year__lte']),
                             )

    return JsonResponse(order_analysis_json(pallets,m))


def chart_trend_api(request):
    if request.method=="POST":
        data = json.loads(request.body)
        m = str(data['m'])
        id = int(data['id'])
        unit = str(data['unit'])
        filterd = data['filter']
    else:
        return JsonResponse({'error':'not available method : GET'})

    if m=='code':
        M = models.Code
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(code=row)

    elif m=='palletcode' :
        M = models.PalletCode
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(palletcode=row)

    else :
        pallets = models.KppPalletData.objects.all()

    # filter 정보를 받아 거른다.
    pallets = pallets.filter(date__year__gte=int(filterd['year__gte']),
                             date__year__lte=int(filterd['year__lte']),
                             )


    # REFERENCE : https://simpleisbetterthancomplex.com/tutorial/2016/07/27/how-to-return-json-encoded-response.html
    return JsonResponse(trend_json(pallets, unit))

def chart_rank_api(request):

    if request.method=="POST":
        data = json.loads(request.body)
        m = str(data['m'])
        key = str(data['key'])
        num = int(data['num'])
        filterd = data['filter']

    num = int(num)
    if m=='code':
        queryset = models.Code.objects.all()
    else :
        queryset = models.PalletCode.objects.all()

    queryset = queryset.filter(kpppalletdata__date__year__gte=int(filterd['year__gte']),
                             kpppalletdata__date__year__lte=int(filterd['year__lte'])
                             )

    if key[1:]=="count":
        queryset = queryset.annotate(key=Count('kpppalletdata'))
    else :
        queryset = queryset.annotate(key=Avg('kpppalletdata__pallet'))

    if key[0]=="-":
        queryset = queryset.order_by(key[0]+"key")[:num+1]
    else :
        queryset = queryset.order_by("key")[:num + 1]


    return JsonResponse(rank_json(queryset, m=m, clean_key=key[1:]))


def list_api(request):
    data=json.loads(request.body)

    m=str(data['m'])
    page=int(data['page'])
    order=str(data['order'])
    filterd=data['filter']

    if m=='code':
        M = models.Code
        queryset=M.objects.all()

    elif m=='company':
        M = models.Company
        queryset = M.objects.all()
    elif m=='palletcode' :
        M = models.PalletCode
        queryset = M.objects.all()

    else :
        queryset = models.KppPalletData.objects.all()

    queryset = queryset.filter(kpppalletdata__date__year__gte=int(filterd['year__gte']),
                             kpppalletdata__date__year__lte=int(filterd['year__lte'])
                             )

    print(filterd['year__gte'], filterd['year__lte'])
    return JsonResponse(list_json(queryset,page, order))

















#3########################################################## LEGACY


# TODO : MENU VIEW 완성하기
# datamanager app 의 첫 페이지
@login_required
def menu_view(request):
    return render(request, "datamanager/menu.html")


'''
login_required() does the following:

If the user isn’t logged in, redirect to settings.LOGIN_URL, passing the current absolute path in the query string. Example: /accounts/login/?next=/polls/3/.
If the user is logged in, execute the view normally. The view code is free to assume the user is logged in.
'''

# TODO : 데이터 업로드 view
# TODO : 데이터 조회 view
# TODO : 데이터 다운로드 view

@login_required
def overview_view(request):

    # kppdata = models.KppPalletData.objects.()

    # 거래량 Top 6 Code 데이터 추출
    codes = models.Code.objects.all()
    pallets = models.KppPalletData.objects.filter(date__year=2017)

    sumlist = []
    for code in codes:
        kpps = pallets.filter(code=code)
        sum = kpps.aggregate(Sum('pallet'))["pallet__sum"]
        if sum==None:
            sum=0
        sumlist.append([sum,code]) #정렬 편하게 하기 위해 sum 을 앞에 둠
    sumlist.sort(reverse=True, key=lambda s:s[0] ) #내림차순 정렬
    topsix = sumlist[:6]


    context = {"topsix" : topsix}
    return render(request, "datamanager/overview.html", context=context)

@login_required
def warning_view(request):
    context = {}
    return render(request, "datamanager/overview.html", context=context)


#TODO: Codelist 페이지 와 codeinfo 페이지와 합치기 (Angular js web app 으로)

#TODO: listview 다양한 방식의 정렬기능 집어넣기
#TODO: listview 클래스 뷰로 만들고 검색기능 추가하기

@login_required
def list_view(request,m="code",page=1):
    page = int(page)
    m = str(m)
    if m=='code':
        M = models.Code
    elif m=='company':
        M = models.Company
    else :
        M = models.PalletCode
    #queryset = M.objects.filter(id__gt=(page - 1) * 50, id__lte=page * 50).annotate(count=Count('kpppalletdata'), avg=Avg('kpppalletdata__pallet'))
    # Count(총 기록 건수 순으로 정렬해서 표시)
    queryset = M.objects.annotate(count=Count('kpppalletdata'), avg=Avg('kpppalletdata__pallet')).order_by('-count')[(page - 1) * 50:page * 50]  #.filter(id__gt=(page - 1) * 50, id__lte=page * 50)

    context={"qset":queryset,
            "prev_next":[page-1,page+1],
            "m":m,
            }
    return render(request, "datamanager/list.html", context=context)


#TODO: info_view 에 google chart 시각화 도입

@login_required
def info_view(request,m="code",id=1):
    m = str(m)
    if m=='code':
        M = models.Code
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(code=row)

    elif m=='company':
        M = models.Company
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(company=row)

    else :
        M = models.PalletCode
        row = M.objects.get(id=id)
        pallets = models.KppPalletData.objects.filter(palletcode=row)

    info = pallets.aggregate(Sum('pallet'), Max('pallet'), Min('pallet'), Avg('pallet'))

    # (sum,year)
    yearsums = [ (pallets.filter(date__year=n).aggregate(Sum('pallet'))['pallet__sum'],n) for n in range(2010,2018)]
    # (sum,month)
    monthsums = [(pallets.filter(date__month=n).aggregate(Sum('pallet'))['pallet__sum'],n) for n in range(1,13)]
    # (sum,weekday)
    weekdaysums = [(pallets.filter(date__week_day=n).aggregate(Sum('pallet'))['pallet__sum'],n) for n in range(1,8)]

    context = {
        "m":m,
        "row" : row,
        "pallets" : pallets,
        "info" : info,
        "yearsums" : yearsums,
        "monthsums" : monthsums,
        "weekdaysums":weekdaysums
    }

    return render(request, "datamanager/info.html", context=context)


