import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avocado_project.settings")
import django
django.setup()


from predict_app import models

import pandas as pd


def make_company_list(dflist):
    result = set()
    for df in dflist:
        result = set(list(result) + list(set(df["업체명"])))

    return list(result)

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


company_list = make_company_list(dflist)
print("(9/10) generate company list complete!")

for name in company_list:
    company = models.Company(name=name)
    company.save()
print("(10/10) save to database complete!")

