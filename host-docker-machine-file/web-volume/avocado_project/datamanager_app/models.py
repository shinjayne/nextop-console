from django.db import models

# Create your models here.

# KPP 에서 제공받은 데이터를 저장
# 납품 / 회수 된 파레트 수량의 모든 기록

# TODO : PalletCode 필드를 ForgienKey Field 로 변경해야함
class KppPalletData(models.Model):
    # (real value, explaination)
    TYPECHOICES = (('OUT','납품(직송포함)'),
                   ('IN','회수'),
                   )

    type = models.CharField(max_length = 10, choices= TYPECHOICES, null=True )
    date = models.DateTimeField(null = True)
    code = models.ForeignKey('Code',null = True, on_delete=models.SET_NULL)
    palletcode = models.ForeignKey('PalletCode', null=True, on_delete=models.SET_NULL)
    pallet = models.IntegerField(null=True)

    def __str__(self):
        return "id = " + str(self.id) + " : " + str(self.date)[:11] +" 수량 "+ str(self.pallet) + " / 코드 : " + str(self.code) + " / 파레트코드 : " + str(self.palletcode)

# Code - Company : many to one relations

# TODO : 기업명 데이터와 코드 규칙 로지스올로부터 전달받아서 이부분 완성하기

class Code(models.Model):
    code = models.CharField(max_length = 10)
    # company = models.ForeignKey('Company' , null=True , on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+ " : " + str(self.code)  # + " ( " + str(self.company) + " ) "

class PalletCode(models.Model):
    palletcode = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.palletcode)

class Company(models.Model):
    name = models.CharField(max_length = 20, unique=True)

    def __str__(self):
        return str(self.id)+" : "+str(self.name)