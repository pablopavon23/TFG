# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class ClinicaFuenlabrada1Medidas(models.Model):
    id_medida = models.BigAutoField(primary_key=True)
    id_sensor = models.IntegerField(blank=True, null=True)
    tipo_medida = models.CharField(max_length=20, blank=True, null=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    id_mota = models.BigIntegerField(blank=True, null=True)
    medida = models.FloatField(blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clinica_fuenlabrada_1_medidas'


class ClinicaFuenlabrada1Motas(models.Model):
    id_mota = models.BigAutoField(primary_key=True)
    mac = models.BigIntegerField(blank=True, null=True)
    num_sensores = models.IntegerField(blank=True, null=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    ultima_conexion = models.DateTimeField(blank=True, null=True)
    ultima_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clinica_fuenlabrada_1_motas'


class ClinicaFuenlabrada1Sensores(models.Model):
    id_sensor = models.AutoField(primary_key=True)
    id_mota = models.BigIntegerField(blank=True, null=True)
    puerto = models.IntegerField(blank=True, null=True)
    tipo_sensor = models.CharField(max_length=20, blank=True, null=True)
    tipo_medida = models.CharField(max_length=20, blank=True, null=True)
    seq = models.BigIntegerField(blank=True, null=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clinica_fuenlabrada_1_sensores'
