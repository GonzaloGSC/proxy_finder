from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import json
from ast import literal_eval # Transformación de strings en arreglos/diccionarios, ej.)  literal_eval(string)
from random import randrange # generación de un numero al azar entre 0 y N, ej.) randrange(N)
from datetime import datetime
from django.core import serializers
import time
# import schedule
import sys
import base64
from apscheduler.schedulers.background import BackgroundScheduler

from django_filters.rest_framework import DjangoFilterBackend # imports de filtros para realizar busquedas.
from rest_framework.filters import OrderingFilter, SearchFilter # imports para ordenar la busqueda.
from rest_framework import generics, status #import para utilizar los tipos de vistas 
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import MProxysAlmacenadosSerializer, MProxysDisponiblesSerializer, MRegistrosSerializer
from .models import MProxysDisponibles, MProxysAlmacenados, MRegistros

#####################################################################################################################################################################################
####################################################################              PROCESOS INTERNOS              ####################################################################
#####################################################################################################################################################################################

class SkipAuth(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return True

def IniciarHarvester():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ObtenerProxys, 'interval', minutes=30)
    scheduler.add_job(ObtenerHtmlYDatos, 'interval', seconds=20)
    scheduler.start()

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes((SkipAuth,))
def ObtenerProxys():#self
    try:
        httpsProxys = []
        httpsProxys.append(requests.get("https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=60&protocols=http%2Chttps&anonymityLevel=elite").json())
        
        httpsProxysAux1 = requests.get("https://www.proxyscan.io/api/proxy?limit=20&type=https&level=elite&uptime=70&ping=400").json() # HTTPS ELITE
        # time.sleep(2)
        # for cosa in requests.get("https://www.proxyscan.io/api/proxy?limit=20&type=https&level=anonymous&uptime=70&ping=400").json(): # HTTPS ANONIMO
        #     httpsProxysAux1.append(cosa)
        time.sleep(2)
        for cosa in requests.get("https://www.proxyscan.io/api/proxy?limit=20&type=http&level=elite&uptime=70&ping=400").json(): # HTTP ELITE
            httpsProxysAux1.append(cosa)
        # time.sleep(2)
        # for cosa in requests.get("https://www.proxyscan.io/api/proxy?limit=20&type=http&level=anonymous&uptime=70&ping=400").json(): # HTTP ANONIMO
        #     httpsProxysAux1.append(cosa)

        httpsProxysAux2 = GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/https/uptime/level1") # HTTPS ELITE
        time.sleep(2)
        for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/https/uptime/level1/2"): 
            httpsProxysAux2.append(cosa)
        time.sleep(2)
        for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/https/uptime/level1/3"):
            httpsProxysAux2.append(cosa)
        time.sleep(2)
        for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/http/uptime/level1"): # HTTP ELITE
            httpsProxysAux2.append(cosa)
        time.sleep(2)
        for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/http/uptime/level1/2"):
            httpsProxysAux2.append(cosa)
        time.sleep(2)
        for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/http/uptime/level1/2"):
            httpsProxysAux2.append(cosa)
        # time.sleep(2)
        # for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/https/uptime/level2"): # HTTPS ANONIMO
        #     httpsProxysAux2.append(cosa)
        # time.sleep(2)
        # for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/https/uptime/level2/2"):
        #     httpsProxysAux2.append(cosa)
        # time.sleep(2)
        # for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/https/uptime/level2/3"):
        #     httpsProxysAux2.append(cosa)
        # time.sleep(2)
        # for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/http/uptime/level2"): # HTTP ANONIMO
        #     httpsProxysAux2.append(cosa)
        # time.sleep(2)
        # for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/http/uptime/level2/2"):
        #     httpsProxysAux2.append(cosa)
        # time.sleep(2)
        # for cosa in GuardarProxysAux2("http://free-proxy.cz/es/proxylist/country/all/http/uptime/level2/23"):
        #     httpsProxysAux2.append(cosa)
        httpsProxysAux3 = []
        # time.sleep(3)
        # httpsProxysAux3.append(requests.get("http://pubproxy.com/api/proxy?http=true&level=elite&limit=20", headers={'User-Agent': 'Chrome'}).json())
        # time.sleep(4)
        # httpsProxysAux3.append(requests.get("http://pubproxy.com/api/proxy?https=true&level=elite&limit=20", headers={'User-Agent': 'Chrome'}).json())
        # time.sleep(4)
        # httpsProxys.append(requests.get("http://pubproxy.com/api/proxy?https=true&level=elite&limit=20", headers={'User-Agent': 'Chrome'}).json())
        arreglo = []
        for cosa in httpsProxys:
            for elem in cosa["data"]:
                if elem["ip"] != "" and elem["port"] != "":
                    arreglo.append({
                        "ip": elem["ip"],
                        "puerto": elem["port"],
                        "protocolo": elem["protocols"][0],
                        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    })
        for cosa in httpsProxysAux1:
            if cosa["Ip"] != "" and cosa["Port"] != "":
                arreglo.append({
                    "ip": cosa["Ip"],
                    "puerto": str(cosa["Port"]),
                    "protocolo": cosa["Type"][0].lower(),
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })  

        for cosa in httpsProxysAux2:
            if cosa["ip"] != "" and cosa["puerto"] != "":
                arreglo.append({
                    "ip": cosa["ip"],
                    "puerto": str(cosa["puerto"]),
                    "protocolo": cosa["protocolo"],
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })  

        print("httpsProxysAux3")
        for cosa in httpsProxysAux3:
            for elem in cosa["data"]:
                if elem["ip"] != "" and elem["port"] != "":
                    arreglo.append({
                        "ip": elem["ip"],
                        "puerto": elem["port"],
                        "protocolo": elem["type"],
                        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    })
        MProxysDisponibles.objects.all().delete()
        for dicc in arreglo:
            MProxysDisponibles.objects.create(ip=dicc["ip"], puerto=dicc["puerto"], protocolo=dicc["protocolo"], fecha=dicc["fecha"])
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Proceso ejecutado con exito.',
            'error': None,
            'data': json.loads(serializers.serialize("json",MProxysDisponibles.objects.all()))
        }
        return Response(response, status.HTTP_200_OK)
    except Exception as e:
        response = {
            'success': False,
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Error al obtener proxys.',
            'error': e.__dict__,
            'data': None,
        }
        return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

def ObtenerDiccionariosProxys(proto):
    proxys = []
    almacenado = True
    try:
        if randrange(10)==1:#proxys almacenados funcionales
            for cosa in json.loads(serializers.serialize("json", MProxysAlmacenados.objects.filter(estado = True))):
                proxys.append(cosa['fields'])
        elif randrange(3)==1: #proxys almacenados (incluye defectuosos para oportunidad de update)
            for cosa in json.loads(serializers.serialize("json", MProxysAlmacenados.objects.filter(estado = False))):
                proxys.append(cosa['fields'])
        else: # proxys externos disponibles
            almacenado = False
            for cosa in json.loads(serializers.serialize("json", MProxysDisponibles.objects.filter())):
                if cosa['fields']["ip"] != "" and cosa['fields']["puerto"] != "":
                    proxys.append(cosa['fields'])
        if len(proxys) == 0:
            return {"estado": False, "almacenado": almacenado, "arreglo": proxys, "error": "No existen proxys con las caracteristicas de busqueda."}
        return {"estado": True, "almacenado": almacenado, "arreglo":proxys, "error": None}
    except Exception as e:
        return {"estado": False, "almacenado": almacenado, "arreglo": proxys, "error": e.__dict__}

# @api_view(['GET'])
# @authentication_classes([])
# @permission_classes((SkipAuth,))
def ObtenerHtmlYDatos():#request
    end = 0.0 #tiempo inicial para evitar errores
    registro = {
        "ip": "",
        "puerto": "",
        "protocolo": "",
        "fecha": "",
        "almacenado": False,
        "estado_respuesta": False,
        "tiempo_respuesta": 0.0,
    }
    arreglo = []
    url = "https://betsapi.com/cin/soccer"
    webpage = requests.get("https://www.google.com/", headers={'User-Agent': 'Chrome'}).content.strip() #req inicial para evitar errores
    intentos = 0
    while intentos < 10:
        time.sleep(1)
        respuesta = ObtenerDiccionariosProxys("https")
        if len(respuesta["arreglo"])>0:
            index = randrange(len(respuesta["arreglo"]))
            proxy = {}
            proxy[respuesta["arreglo"][index]["protocolo"]] = "http://"+respuesta["arreglo"][index]["ip"]+":"+respuesta["arreglo"][index]["puerto"]
            try:
                invalido = False
                for cosa in json.loads(serializers.serialize("json", MProxysAlmacenados.objects.filter(protocolo=respuesta["arreglo"][index]["protocolo"], ip=respuesta["arreglo"][index]["ip"], puerto=respuesta["arreglo"][index]["puerto"], estado=False))):
                    if respuesta["almacenado"] == False:
                        invalido = True
                if invalido == False:
                    start = time.time()
                    webpage = requests.get(url, headers={'User-Agent': 'Chrome'}, proxies = proxy, timeout=15).content.strip()
                    end = time.time() - start
                    soup = BeautifulSoup(webpage, "html.parser")
                    #guarda el proxy en la bdd
                    editar = False
                    for cosa in json.loads(serializers.serialize("json", MProxysAlmacenados.objects.filter(protocolo=respuesta["arreglo"][index]["protocolo"], ip=respuesta["arreglo"][index]["ip"], puerto=respuesta["arreglo"][index]["puerto"]))):
                        instance = MProxysAlmacenados.objects.get(id=cosa["pk"])
                        instance.estado = True
                        instance.fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        instance.save()
                        editar = True
                    if editar == False:
                        MProxysAlmacenados.objects.create(
                            protocolo=respuesta["arreglo"][index]["protocolo"], 
                            ip=respuesta["arreglo"][index]["ip"], 
                            puerto=respuesta["arreglo"][index]["puerto"],
                            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            estado= True)
                    #establece los datos para el registro de transaccion
                    registro["ip"] = respuesta["arreglo"][index]["ip"]
                    registro["puerto"] = respuesta["arreglo"][index]["puerto"]
                    registro["protocolo"] = respuesta["arreglo"][index]["protocolo"]
                    registro["fecha"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    registro["almacenado"] = respuesta["almacenado"]
                    registro["estado_respuesta"] = True
                    registro["tiempo_respuesta"] = format(end, ".5f")
                    #guardar la información enviando el html
                    arreglo = GuardarInfoPagina(soup)
                    intentos = 100 #para terminar while sin break
                    #crea registro de transaccion
                    MRegistros.objects.create(
                        ip = registro["ip"],
                        puerto = registro["puerto"],
                        protocolo = registro["protocolo"],
                        fecha = registro["fecha"],
                        almacenado = registro["almacenado"],
                        estado_respuesta = registro["estado_respuesta"],
                        tiempo_respuesta =  registro["tiempo_respuesta"],
                    )
            except Exception as e:
                editar = False
                for cosa in json.loads(serializers.serialize("json", MProxysAlmacenados.objects.filter(protocolo=respuesta["arreglo"][index]["protocolo"], ip=respuesta["arreglo"][index]["ip"], puerto=respuesta["arreglo"][index]["puerto"]))):
                    instance = MProxysAlmacenados.objects.get(id=cosa["pk"])
                    instance.estado = False
                    instance.fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    instance.save()
                    editar = True
                if editar == False:
                    MProxysAlmacenados.objects.create(
                        protocolo=respuesta["arreglo"][index]["protocolo"], 
                        ip=respuesta["arreglo"][index]["ip"], 
                        puerto=respuesta["arreglo"][index]["puerto"],
                        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        estado= False)
                #establece los datos para el registro de transaccion
                registro["ip"] = respuesta["arreglo"][index]["ip"]
                registro["puerto"] = respuesta["arreglo"][index]["puerto"]
                registro["protocolo"] = respuesta["arreglo"][index]["protocolo"]
                registro["fecha"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                registro["almacenado"] = respuesta["almacenado"]
                registro["estado_respuesta"] = False    
                registro["tiempo_respuesta"] = format(end, ".5f")
                #crea registro de transaccion
                MRegistros.objects.create(
                    ip = registro["ip"],
                    puerto = registro["puerto"],
                    protocolo = registro["protocolo"],
                    fecha = registro["fecha"],
                    almacenado = registro["almacenado"],
                    estado_respuesta = registro["estado_respuesta"],
                    tiempo_respuesta =  registro["tiempo_respuesta"],
                )
            respuesta["arreglo"].pop(index)
            
        intentos = intentos+1
    response = {
        'success': True,
        'status_code': status.HTTP_200_OK,
        'message': 'Proceso ejecutado con exito.',
        'error': None,
        'data': arreglo
    }
    return Response(response, status.HTTP_200_OK)
    
def GuardarInfoPagina(soup):
    # try:
    tabla = soup.find("table", attrs={"class": "table table-sm"})
    arregloFilas = tabla.find_all("tr")
    arregloFinal = []
    for fila in arregloFilas:
        contador = 0
        diccionario = {
            "competicion": "",
            "tiempo": "",
            "equipo1": "",
            "marcador": "",
            "equipo2": "",
            "cuotaEquipo1": "",
            "cuotaEmpate": "",
            "cuotaEquipo2": "",
        }
        for columna in fila.find_all("td"):
            if contador == 0:
                diccionario["competicion"] = columna.a.text
            if contador == 1:
                diccionario["tiempo"] = columna.span.text.replace("'","").replace("<sup>","").replace("</sup>","")
            if contador == 2:
                diccionario["equipo1"] = columna.a.text
            if contador == 3:
                diccionario["marcador"] = columna.a.text
            if contador == 4:
                diccionario["equipo2"] = columna.a.text
            if contador == 5:
                diccionario['cuotaEquipo1'] = columna.text
            if contador == 6:
                diccionario["cuotaEmpate"] = columna.text
            if contador == 7:
                diccionario["cuotaEquipo2"] = columna.text
            if contador >= 7:
                valido = True;
                for dic in arregloFinal:
                    if dic == diccionario:
                        valido = False
                if valido:
                    arregloFinal.append(diccionario)
            contador = contador + 1
    # print("arreglo creado")
    # {'competicion': 'Italy Serie C Cup', 
    # 'tiempo': '118', 
    # 'equipo1': 'Matelica', 
    # 'marcador': '1-1', 
    # 'equipo2': 'Aquila 1902 Montevarchi', 
    # 'cuotaEquipo1': '13.000', 
    # 'cuotaEmpate': '1.035', 
    # 'cuotaEquipo2': '21.000'}




    #     response = {
    #         'success': True,
    #         'status_code': status.HTTP_201_CREATED,
    #         'message': 'Proceso ejecutado con exito.',
    #         'error': None,
    #         'data': arregloFinal
    #     }
    #     return Response(response, status.HTTP_201_CREATED)
    # except Exception as e:
    #     response = {
    #         'success': False,
    #         'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         'message': 'Error al guardar la información de la pagina.',
    #         'error': e.__dict__,
    #         'data': None,
    #     }
    #     return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

def GuardarProxysAux2(url):
    webpage = requests.get(url, headers={'User-Agent': 'Chrome'}).content.strip()
    soup = BeautifulSoup(webpage, "html.parser")
    tabla = soup.find("table", attrs={"id":"proxy_list"})
    arregloFilas = tabla.find("tbody").find_all("tr")
    arregloFinal = []
    
    for fila in arregloFilas:
        contador = 0
        diccionario = {
            "ip": "",
            "puerto": "",
            "protocolo": ""
        }
        for columna in fila.find_all("td"):
            if contador == 0:
                try:
                    diccionario["ip"] = columna.script.string.replace('document.write(Base64.decode("', '').replace('"))', '')
                    base64_bytes = diccionario["ip"].encode('ascii')
                    message_bytes = base64.b64decode(base64_bytes)
                    diccionario["ip"]  = message_bytes.decode('ascii')
                except:
                    pass
            if contador == 1:
                try:
                    diccionario["puerto"] = columna.span.text
                except:
                    pass
            if contador == 2:
                try:
                    diccionario["protocolo"] = columna.small.text.lower()
                except:
                    pass
            if contador >= 2:
                valido = True;
                for dic in arregloFinal:
                    if dic == diccionario:
                        valido = False
                
                if valido and diccionario["ip"] != '' and diccionario["puerto"] != '' and diccionario["protocolo"] != '' and diccionario["protocolo"] != "socks4" and diccionario["protocolo"] != "socks5":
                    arregloFinal.append(diccionario)
            contador = contador + 1   
    return arregloFinal

def GuardarProxysAux3(url):
    # req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    # webpage = urlopen(req).read()

    webpage = requests.get(url, headers={'User-Agent': 'Chrome'}, timeout=4).content.strip()
    soup = BeautifulSoup(webpage, "html.parser")
    for el in soup.find_all("table", {"class":"DataGrid"}):
        tabla = el
    # tabla = soup.find("table", attrs={"class":"DataGrid"})
    arregloFilas = tabla.find("tbody").find_all("tr")
    arregloFinal = []
    # for fila in arregloFilas:
    #     contador = 0
    #     diccionario = {
    #         "ip": "",
    #         "puerto": "",
    #     }
    #     for columna in fila.find_all("td"):
    #         if contador == 0:
    #             try:
    #                 diccionario["ip"] = columna.script.string.replace('document.write(Base64.decode("', '').replace('"))', '')
    #                 base64_bytes = diccionario["ip"].encode('ascii')
    #                 message_bytes = base64.b64decode(base64_bytes)
    #                 diccionario["ip"]  = message_bytes.decode('ascii')
    #             except:
    #                 pass
    #         if contador == 1:
    #             try:
    #                 diccionario["puerto"] = columna.span.text
    #             except:
    #                 pass
    #         if contador >= 1:
    #             valido = True;
    #             for dic in arregloFinal:
    #                 if dic == diccionario:
    #                     valido = False
                
    #             if valido and diccionario["ip"] != '' and diccionario["puerto"] != '':
    #                 arregloFinal.append(diccionario)
    #         contador = contador + 1   
    # return arregloFinal


###################################################################################################################################################################################
####################################################################              CONSULTAS UTILES              ####################################################################
###################################################################################################################################################################################

class SP_VerProxysDisponibles(generics.ListAPIView): 
    serializer_class = MProxysDisponiblesSerializer
    permission_classes = (AllowAny,)
    queryset = MProxysDisponibles.objects.all() 
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)#, OrderingFilter, SearchFilter, DjangoFilterBackend)
    data = ('id','ip','puerto','protocolo', 'fecha')
    filter_fields = data
    ordering_fields = data
    search_fields = data

class SP_VerProxysAlmacenados(generics.ListAPIView): 
    serializer_class = MProxysAlmacenadosSerializer
    permission_classes = (AllowAny,)
    queryset = MProxysAlmacenados.objects.all() 
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)#, OrderingFilter, SearchFilter, DjangoFilterBackend)
    data = ('id','ip','puerto','protocolo', 'estado' , 'fecha')
    filter_fields = data
    ordering_fields = data
    search_fields = data

class SP_VerRegistros(generics.ListAPIView): 
    serializer_class = MRegistrosSerializer
    permission_classes = (AllowAny,)
    queryset = MRegistros.objects.all() 
    filter_backends = (OrderingFilter, DjangoFilterBackend, SearchFilter)#, OrderingFilter, SearchFilter, DjangoFilterBackend)
    data = ('id','ip','puerto','protocolo', 'almacenado' , 'fecha', 'estado_respuesta', 'tiempo_respuesta')
    filter_fields = data
    ordering_fields = data
    search_fields = data


