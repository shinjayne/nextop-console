import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avocado_project.settings")
import django
django.setup()


from datamanager_app import models

import pandas as pd


def make_company_list(dflist):
    result = set()
    for df in dflist:
        result = set(list(result) + list(set(df["유형코드"])))

    return list(result)

csvlist = [
    '_csvs/in10-12/2010.csv',
    '_csvs/in10-12/2010(1).csv',
    '_csvs/in10-12/2010(2).csv',
    '_csvs/in10-12/2011.csv',
    '_csvs/in10-12/2011(1).csv',
    '_csvs/in10-12/2011(2).csv',

]

dflist = []
for csv in csvlist :
    dflist.append(pd.read_csv(csv))

print("(1~8/10) make df complete!")

palletcodelist = make_company_list(dflist)
print("(9/10) generate company list complete!")

for name in palletcodelist:
    try :
        name= str(int(name))
    except:
        name='nan'
    try :
        #이미 존재하는 코드인지 확인
        exsist = models.PalletCode.objects.get(palletcode=name)


    except :
        #존재하지 않는다면 추가
        company = models.PalletCode(palletcode=name)
        company.save()
print("(10/10) save to database complete!")

