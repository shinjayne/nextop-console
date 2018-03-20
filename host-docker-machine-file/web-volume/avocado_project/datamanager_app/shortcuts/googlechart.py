from django.db.models import Sum, Avg, Max, Min, Count

def order_rank_json(kpp_queryset, model, items):
    data = {
        'cols':[
            {'id': 'A', 'label': '파레트코드+이산수량',  'type' : 'string'},
            {'id':'B', 'label':'횟수', 'type' :'number'},
        ],
        'rows':[]
    }

    if model=='code':
        # 한 기업의 거래 내역에 대해서, 가장 많이 등장하는 파레트유형 순으로 파레트 유형 정렬
        #palletcode_top_three = items.annotate(pallet_count = Count(kpp_queryset)).order_by('-pallet_count')[:3]
        # 결과값이 담겨질 리스트
        answerset = []
        for pc in items:
            filtered = kpp_queryset.filter(palletcode=pc)
            palletset_ordered = list(set(datarow.pallet for datarow in filtered))
            palletset_ordered.sort(reverse=True)


            for p in palletset_ordered:
                howmany = filtered.filter(pallet=p).count()
                answerset.append([howmany, pc.palletcode, p])

        answerset.sort(reverse=True)
        # answerset 에서는 [횟수 , 파레트유형, 주문수량] 순으로 들어가 있다.
        for a in answerset:
            rowname = str(a[1]) + '를 ' + str(a[2]) + '개씩'
            cell = {'c': [
                {'v': rowname, 'f': rowname},
                {'v': a[0], 'f': str(a[0])}
            ]}
            data['rows'].append(cell)

    else : #model=='palletcode'
        answerset = []
        codes = list(set(kpp.code for kpp in kpp_queryset))
        for c in codes:
            filtered = kpp_queryset.filter(code=c)
            palletset_ordered = list(set(datarow.pallet for datarow in filtered))
            palletset_ordered.sort(reverse=True)


            for p in palletset_ordered:
                howmany = filtered.filter(pallet=p).count()
                answerset.append([howmany, c.code, p])

        answerset.sort(reverse=True)
        # answerset 에서는 [횟수 , 기업코드, 주문수량] 순으로 들어가 있다.
        for a in answerset:
            rowname = str(a[1]) + '기업서 ' + str(a[2]) + '개씩'
            cell = {'c': [
                {'v': rowname, 'f': rowname},
                {'v': a[0], 'f': str(a[0])}
            ]}
            data['rows'].append(cell)


    return data

def order_analysis_json(kpp_queryset,model):

    data = {
        'cols':[
            {'id': 'A', 'label': 'date',  'type' : 'string'},
            {'id':'B', 'label':'OUT pallet', 'type' :'number'}
        ],
        'rows':[]
    }

    # for plotting chart
    kpp_queryset = kpp_queryset.order_by('date')

    for one_q in kpp_queryset:
        pretty_datestr = str(one_q.date)[:10]
        if model=="code":
            pretty_palletstr = str(one_q.palletcode.palletcode) + " 를 " + str(one_q.pallet) +"개"
        else :
            pretty_palletstr = str(one_q.code.code) + " 기업서 " + str(one_q.pallet) + "개"
        cell = {'c': [
            {'v': str(pretty_datestr), 'f': str(pretty_datestr)},
            {'v': one_q.pallet, 'f' : pretty_palletstr},
        ]}

        data['rows'].append(cell)

    return data





def trend_json(queryset,unit="year"):
    '''
    :param queryset: 트렌드 합산치를 계산하고싶은 쿼리셋 (pallet 라는 컬럼이 반드시 존재해야함)
    :param unit: Choice amonge year,month,weekday,day__year,day__month
    :return: data[dictionary]
    '''

    data = {
        'cols':[
            {'id': 'A', 'label': 'date',  'type' : 'string'},
            {'id':'B', 'label':'OUT Sum', 'type' :'number'},
            {'id':'C', 'label':'IN Sum', 'type' : 'number'}
        ],
        'rows':[]
    }


    if unit=="year":
        #(sum,date)
        sums = [(queryset.filter(date__year=n).aggregate(Sum('pallet'))['pallet__sum'], n) for n in
                    range(2010, 2018)]
    elif unit=="month":
        # (sum,date)
        sums = [(queryset.filter(date__month=n).aggregate(Sum('pallet'))['pallet__sum'], n) for n in range(1, 13)]

    elif unit=="weekday" :
        # (sum,date)
        labels=["토","일",'월','화','수','목','금','토']
        sums = [(queryset.filter(date__week_day=n).aggregate(Sum('pallet'))['pallet__sum'], labels[n]) for n in
                       range(1, 8)]

    elif unit=="day__year" :
        # (sum,date)
        datelist = queryset.filter(date__year=2017).values('date').annotate(pallet__sum=Sum('pallet')).order_by('date')
        sums = [(dt['pallet__sum'], dt['date']) for dt in datelist]

    elif unit=="day__month":
        data = {
            'cols': [
                {'id': 'A', 'label': 'date', 'type': 'string'},
            ],
            'rows': []
        }
        for month in range(1,13):
            data['cols'].append({
                'id':str(month)+'월',
                'label':str(month)+'월',
                'type':'number'
            })


        #일별로 파레트 총합 합산합니다.
        only2017 = queryset.filter(date__year=2017).values('date').annotate(pallet__sum=Sum('pallet')).order_by('date')


        for day in range(1,32):
            cell = {'c':[
                {'v':str(day), 'f':str(day)},
            ]}
            #12줄이 추가됨
            #누적수치
            for month in range(1,13):
                day_cumulate = only2017.filter(date__month=month, date__day__lte=day).aggregate(cumulate=Sum('pallet__sum'))['cumulate']
                cell['c'].append({
                    'v': day_cumulate,
                    'f': str(day_cumulate)
                })

            data['rows'].append(cell)

        return data

    elif unit=="day__week":
        data = {
            'cols': [
                {'id': 'A', 'label': 'date', 'type': 'string'},
            ],
            'rows': []
        }
        for week in range(1,10):
            data['cols'].append({
                'id':str(week)+'째주',
                'label':str(week)+'째주',
                'type':'number'
            })



        datelist = queryset.values('date').annotate(pallet__sum=Sum('pallet')).order_by('date')
        only2017 = datelist.filter(date__year=2017)

        #월화수목금토일
        weekstr=['토','일','월','화','수','목','금','토','일']
        for weekday in range(1,8):
            daylist = []
            for week in range(1,10):
                try:
                    day = only2017.get(date__week=week, date__week_day=weekday)['pallet__sum']
                except:
                    day = 0
                daylist.append(day)

            #첫번째줄
            cell = {'c':[
                {'v':weekstr[weekday], 'f':weekstr[weekday]},
            ]}
            for day in daylist:
                cell['c'].append({
                    'v': day,
                    'f': str(day)
                })

            data['rows'].append(cell)

        return data


    for ys in sums:

        cell = {'c':[
            {'v' : str(ys[1]), 'f':str(ys[1])},
            {'v' : ys[0],'f':str(ys[0])}
        ]}

        data["rows"].append(cell)

    return data


def rank_json(queryset,m,clean_key):

    data = {
        'cols':[
            {'id': 'A', 'label': m,  'type' : 'string'},
            {'id':'B', 'label':clean_key, 'type' :'number'}
        ],
        'rows':[]
    }
    if m=="code":
        for q in queryset:
            cell = {'c':[
                {'v':str(q.code),'f':str(q.code)},
                {'v':str(q.key),'f':str(q.key)}
            ]}
            data["rows"].append(cell)
    else :
        for q in queryset:
            cell = {'c':[
                {'v':str(q.palletcode),'f':str(q.palletcode)},
                {'v':str(q.key),'f':str(q.key)}
            ]}
            data["rows"].append(cell)

    return data