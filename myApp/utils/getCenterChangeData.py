import json
import time
from  .getPublicData import *
import re
def getCircleData():
    cars=list(getAllCars())
    oilData=[]
    eletricdatas=[]
    for i in cars:
        if i.energyType=='汽油':
            oilData.append([i.carName,i.saleVolume,i.energyType])
        elif i.energyType=='纯电动':
            eletricdatas.append([i.carName,i.saleVolume,i.energyType])
    oilData=oilData[:10]
    eletricdatas=eletricdatas[:10]
    return oilData,eletricdatas