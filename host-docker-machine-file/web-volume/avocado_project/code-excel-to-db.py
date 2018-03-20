import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avocado_project.settings")
import django
django.setup()


from datamanager_app import models

import pandas as pd


def make_company_list(dflist):
    result = set()
    for df in dflist:
        result = set(list(result) + list(set(df["코드"])))

    return list(result)

csvlist = [
    '_csvs/in10-12/2010.csv',
    '_csvs/in10-12/2010(1).csv',
    '_csvs/in10-12/2010(2).csv',
    '_csvs/in10-12/2011.csv',
    '_csvs/in10-12/2011(1).csv',
    '_csvs/in10-12/2011(2).csv',
    '_csvs/in10-12/2012.csv',
    '_csvs/in10-12/2012(1).csv',
    '_csvs/in10-12/2012(2).csv',
]

dflist = []
for csv in csvlist :
    dflist.append(pd.read_csv(csv))

print("(1~8/10) make df complete!")

codelist = make_company_list(dflist)
print("(9/10) generate company list complete!")

for name in codelist:
    try :
        #이미 존재하는 코드인지 확인
        exsist = models.Code.objects.get(code=name)


    except :
        #존재하지 않는다면 추가
        company = models.Code(code=name)
        company.save()
print("(10/10) save to database complete!")

