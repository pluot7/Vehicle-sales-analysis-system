from myApp.models import *

def getAllCars():
    return CarInfomation.objects.all()