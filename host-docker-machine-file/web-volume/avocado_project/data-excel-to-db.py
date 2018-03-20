import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avocado_project.settings")
import django
django.setup()

from datamanager_app import models

from datetime import datetime

import pandas as pd

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


for df in dflist:
    compact = df[["코드", "발송일", "유형코드", "수량"]]

    long = len(df)
    for i in range(long):
        row = list(compact.iloc[i])
        type = "IN"
        code = models.Code.objects.get(code=str(int(row[0])))
        date = datetime(int(str(row[1])[:4]), int(str(row[1])[4:6]), int(str(row[1])[6:]))
        palletcode = models.PalletCode.objects.get(palletcode = str(int(row[2])))

        try :
            pallet = int(row[3].replace('-','').strip().replace(',',''))
        except :
            pallet = int(-404)

        if i%1000 == 0 :
            print("ok running ,,,")

        try :
            exsist = models.KppPalletData.objects.filter(date=date).filter(code=code).get(pallet=pallet)
            exsist.palletcode = palletcode
            exsist.type="IN"
            exsist.save()


        except :
            pallet_data = models.KppPalletData(type=type, code=code, date=date, palletcode=palletcode, pallet=pallet)
            pallet_data.save()
            #print("############ ?! Add New!? ##############")
            #print("############" ,date,"/", pallet,"개/" )



