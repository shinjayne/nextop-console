import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avocado_project.settings")
import django
django.setup()

from predict_app import models

import pandas as pd

df2010 = pd.read_excel('kpp_data.xlsx', sheetname='2010년')
print("(1/10) dataframe 2010  read complete!")
df2011 = pd.read_excel('kpp_data.xlsx', sheetname='2011년')
print("(2/10) dataframe 2011  read complete!")
df2012 = pd.read_excel('kpp_data.xlsx', sheetname='2012년')
print("(3/10) dataframe 2012  read complete!")
df2013 = pd.read_excel('kpp_data.xlsx', sheetname='2013년')
print("(4/10) dataframe 2013  read complete!")
df2014 = pd.read_excel('kpp_data.xlsx', sheetname='2014년')
print("(5/10) dataframe 2014  read complete!")
df2015 = pd.read_excel('kpp_data.xlsx', sheetname='2015년')
print("(6/10) dataframe 2015  read complete!")
df2016 = pd.read_excel('kpp_data.xlsx', sheetname='2016년')
print("(7/10) dataframe 2016  read complete!")
df2017 = pd.read_excel('kpp_data.xlsx', sheetname='201708')
print("(8/10) dataframe 2017  read complete!")

dflist = [df2010, df2011,df2012, df2013, df2014, df2015, df2016 , df2017]

for df in dflist:
    compact = df[["년월", "DPT_NAM", "EMP_NAM", "업체명", "투입수량","코드"]]

    long = len(df)
    for i in range(long):
        row = list(compact.iloc[i])
        date = row[0].to_pydatetime()
        department = row[1]
        manager = row[2]
        company = models.Company.objects.get(name=row[3])
        pallet_out = row[4]
        code = str(row[5])

        try :
            exsist = models.PalletData.objects.filter(date=date).filter(company=company).get(pallet_out=pallet_out)
            exsist.code = code
            exsist.save()

        except :
            pallet_data = models.PalletData(date=date, department=department, manager=manager, company=company,
                                            pallet_out=pallet_out, code=code)
            pallet_data.save()



