from django.db import models

class MProxysDisponibles(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=120, null=False, blank=False)
    puerto = models.CharField(max_length=120, null=False, blank=False)
    protocolo = models.CharField(max_length=120, null=False, blank=False)
    fecha = models.CharField(max_length=120)
    def __str__(self):
        return self.protocolo +" "+ self.ip + ":" + self.puerto

class MProxysAlmacenados(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=120, null=False, blank=False)
    puerto = models.CharField(max_length=120, null=False, blank=False)
    protocolo = models.CharField(max_length=120, null=False, blank=False)
    fecha = models.CharField(max_length=120)
    estado = models.BooleanField(null=False, blank=False)
    def __str__(self):
        return self.protocolo +" "+ self.ip + ":" + self.puerto

class MRegistros(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=120, null=False, blank=False)
    puerto = models.CharField(max_length=120, null=False, blank=False)
    protocolo = models.CharField(max_length=120, null=False, blank=False)
    fecha = models.CharField(max_length=120)
    almacenado = models.BooleanField(null=False, blank=False)
    estado_respuesta = models.BooleanField(null=False, blank=False)
    tiempo_respuesta = models.DecimalField(max_digits=19, decimal_places=5, null=False, blank=False)
    def __str__(self):
        return self.protocolo +" "+ self.ip + ":" + self.puerto