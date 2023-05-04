'''
plate_preparation_60ml
Generate a worklist for plate_preparation_60ml method on Hamilton
Script: Ludivine Profit
Last update: 2020/12/03
'''

from WLreadWrite import *
from excelRead import *
from math import*
from simpleFunctions import*

path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\Plate_preparation.xlsx'
worklistPath=r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\WL\WL_plate_preparation.txt'

pathPlate = r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\WL\plate.txt'
pathComponent = r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\WL\component.txt'

#Get back excel synthesis sheet
Plates_sheet=getExcelSheet(path)

#Read current plate number from 1 to 5
plateNbr=getComponentPlateNbr(pathPlate)
print('plate=' + str(plateNbr))

#Read current component number from 0 (water) to 12
componentNbr=getComponentPlateNbr(pathComponent)
print('component=' + str(componentNbr))

#Opening worklist file
WLfile = open(worklistPath, "w")

#Write column names (Script variables)
writeVariableName(WLfile)

#Extract plate and component info from Excel
plate = getPlate(Plates_sheet, plateNbr)
while plate[1] == "":
    plateNbr = plateNbr + 1
    if plateNbr == 6:
        writeComponentPlateNbr(pathPlate, "Plate", plateNbr)
        quit()
    else:
        plate = getPlate(Plates_sheet, plateNbr)
        componentNbr = 0

if componentNbr == 0:
    # Calcul total volume for the plate
    totVolumes = []
    for i in range(96):
        totVolumes.append(0)
    for j in range(1, 13):
        component = getComponent(Plates_sheet, plate[0], j)
        concentration = getConcentration(Plates_sheet, plate[0], component[0])
        if component[1] != "":
            volumes = getVolumes(component[3], plate[3], concentration)
            for vol in range(96):
                totVolumes[vol] = totVolumes[vol] + volumes[vol]
    print("tot vol", totVolumes)
    # Calcul water volumes
    volumes = getWaterVolumes(plate[3], totVolumes)
    # Component water ID = 1
    # Water position on deck = "water"
    component[1] = "1"
    component[2] = "water"
    if volumes.count(0) == 96:
        componentNbr = componentNbr + 1

if componentNbr != 0:
    component = getComponent(Plates_sheet, plate[0], componentNbr)
    while component[1] == "":
        componentNbr = componentNbr + 1
        component = getComponent(Plates_sheet, plate[0], componentNbr)
        if componentNbr == 13:
            plateNbr = plateNbr + 1
            componentNbr = 0
            # Write current component and plate number
            writeComponentPlateNbr(pathComponent, "Component", componentNbr)
            writeComponentPlateNbr(pathPlate, "Plate", plateNbr)
            quit()
    print("component = ", component)

    concentration = getConcentration(Plates_sheet, plate[0], component[0])
    # Calcul volumes
    volumes = getVolumes(component[3], plate[3], concentration)

#if vol > 950: multiplicator x = 2
x = 1  # multiplicator
volMax=max(volumes)
x=ceil(volMax/940)
print("x = ", x)
if x > 1:
    i = 0
    for vol in volumes:
        volumes[i]=round(vol/x,2)
        i=i+1

print("plate = ", plate)
print("concentration =", concentration)
print("volumes = ", volumes)
wells = getWells(volumes)
aspVolDispCol = getAspVolDispCol(volumes)
aspVolVol = aspVolDispCol[0]
dispColCol = aspVolDispCol[1]
tipType = str(getOneTipType(volumes))
tipMaskStr = getTipMask(volumes)
j = 0

for aspVol in aspVolVol:
        aspVolStr = getAspVolStr(aspVol)
        aspMask = getAspDispMask(aspVol)
        aspMaskStr = getAspDispMaskStr(aspMask)
        if aspMaskStr != "00000000":
            for i in range (x): #write x times asp/disp actions
                aspDispMode = "0"
                writeVariable(WLfile,component[1], aspDispMode, component[2], tipType, tipMaskStr, aspVolStr, aspMaskStr,"seq")
                dispCol=dispColCol[j]
                for column in dispCol:
                    dispVol = getDispVol(volumes, column)
                    dispVolStr = getDispVolStr(dispVol)
                    dispMask = getAspDispMask(dispVol)
                    dispMaskStr = getAspDispMaskStr(dispMask)
                    dispSeqStr=getDispSeqStr(wells,column)
                    if dispMaskStr != "00000000":
                        aspDispMode = "1"
                        writeVariable(WLfile,component[1], aspDispMode, plate[2], tipType, tipMaskStr, dispVolStr, dispMaskStr, dispSeqStr)
            j = j + 1
WLfile.close()

#move on to next component
componentNbr=componentNbr+1

if componentNbr == 13:
    #move on to next plate, first component
    componentNbr=0
    plateNbr = plateNbr+1

#Write current component and plate number
writeComponentPlateNbr(pathComponent, "Component", componentNbr)
writeComponentPlateNbr(pathPlate, "Plate", plateNbr)









