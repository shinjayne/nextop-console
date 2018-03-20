from rest_framework import serializers

from . import models

class KppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KppPalletData
        fields = ('id', 'date', 'code', 'palletcode','pallet')

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Code
        fields = ('id', 'code')

class PalletCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PalletCode
        fields = ('id', 'palletcode')