from .. import serializers
from django.db.models import Sum, Avg, Max, Min, Count
from django.db import models

def list_json(queryset, page, order):
    '''
    if m=='code':
        ser=serializers.CodeSerializer
    elif m=='palletcode' :
        ser=serializers.PalletCodeSerializer

    else :
        ser=serializers.KppSerializer
    '''
    data = {
        "list":[],
        'howmany':0
    }

    # avg 와 count 정보를 담는다
    # avg 는 소숫점 2번째 자리에서 끊는다 (django DecimalField)
    v_queryset = queryset.values()
    v_queryset = v_queryset.annotate(avg=Avg('kpppalletdata__pallet', output_field=models.IntegerField()), count=Count('kpppalletdata'), sum=Sum('kpppalletdata__pallet'))
    data['howmany'] = v_queryset.count()
    v_queryset = v_queryset.order_by(order)[(page-1)*50:page*50]

    for q in v_queryset:
        row=q
        data["list"].append(row)



    return data