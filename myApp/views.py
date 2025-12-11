from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
# Create your views here.
from  .utils import  getCenterData
from  .utils import getPublicData
from  .utils import getCenterLeftData
from  .utils import  getBottomLeftData
from  .utils import  getCenterRightData
from .utils import  getCenterChangeData
from .utils import getBottomRightData

def center(request):

    if request.method=='GET':
        sumCar,highVolume,topCar,mostModdel ,mostBrand,averagePrices=getCenterData.getBaseData()
        lastSortList= getCenterData.getRollData()
        oilRate,electricRate,mixRate=getCenterData.getTypeRate()
        return JsonResponse({
            'sumCar':sumCar,
            'highVolume':highVolume,
            'topCar':topCar,
            'mostModdel':mostModdel,
            'mostBrand':mostBrand,
            'averagePrices':averagePrices,
            'oilRate':oilRate,
            'lastSortList':lastSortList,
            'electricRate': electricRate,
            'mixRate': mixRate,



        })

def centerLeft(request):
    if request.method=='GET':
        lastPeiList=getCenterLeftData.getPieBrand()
        return JsonResponse({
                'lastPeiList':lastPeiList,



        })

def bottomLeft(request):
    if request.method == 'GET':
        brandList,volumeList,priceList=getBottomLeftData.getSquareData()
        return JsonResponse({
        'brandList':brandList,
        'volumeList':volumeList,
        'priceList':priceList

        })

def centerRight(request):
    if request.method == 'GET':
        realData=getCenterRightData.getPriceSortDate()
        return JsonResponse({
            'realData':realData
        })

def centerRightChange(request,energyType):
    if request.method == 'GET':
        oilData,eletricdatas=getCenterChangeData.getCircleData()
        realData=[]
        if energyType==1:
            realData=oilData
        else:
            realData=eletricdatas
        return JsonResponse({
            'realData':realData,
        })

def bottomRight(request):
    if request.method == 'GET':
        carData=getBottomRightData.getRankData()

        return JsonResponse({
            'carData':carData
        })