from django.apps import AppConfig


class HarvesterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.harvester'
    # def ready(self):##Inicia el proceso de harvester para recolección automatica
    #     from .views import IniciarHarvester
    #     IniciarHarvester()
