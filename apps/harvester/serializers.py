from rest_framework import serializers
from .models import MProxysDisponibles, MProxysAlmacenados, MRegistros

class MProxysDisponiblesSerializer (serializers.ModelSerializer):
    class Meta:
        model = MProxysDisponibles
        fields = [
            'id',
            'ip',
            'puerto',
            'protocolo',
            'fecha',
        ]

class MProxysAlmacenadosSerializer (serializers.ModelSerializer):
    class Meta:
        model = MProxysAlmacenados
        fields = [
            'id',
            'ip',
            'puerto',
            'protocolo',
            'fecha',
            'estado',
        ]

class MRegistrosSerializer (serializers.ModelSerializer):
    class Meta:
        model = MRegistros
        fields = [
            'id',
            'ip',
            'puerto',
            'protocolo',
            'fecha',
            'almacenado',
            'estado_respuesta',
            'tiempo_respuesta',
        ]   
