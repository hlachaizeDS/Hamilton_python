'''
Generate a worklist with number of tips required per tip type for plate_preparation_60ml method on Hamilton
Script: Ludivine Profit
Last update: 2020/12/03
'''

from excelRead import *
from simpleFunctions import *
import math

path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\Plate_preparation.xlsx'
WLPath=r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\WL\WL_neededTip.txt'

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

#Get back excel sheet
Plates_sheet=getExcelSheet(path)

def getNeededTips(Plates_sheet):
    tip1000 = 0
    tip300 = 0
    tip50 = 0
    neededTips = [tip1000,tip300,tip50]
    for i in range (1,6):
        plate=getPlate(Plates_sheet,i)
        if plate[1] != "":
            print("plate = ", plate)
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
            if volumes.count(0) != 96:
                # get needed tips
                tipType = getOneTipType(volumes)
                aspTotVol = [0, 0, 0, 0, 0, 0, 0, 0]
                for i in range(8):
                    for col in range (12):
                        aspTotVol[i] = aspTotVol[i] + volumes[col * 8 + i]
                    if aspTotVol[i] != 0:
                        if tipType == "1000":
                            tip1000 = tip1000 + 1
                        if tipType == "300":
                            tip300 = tip300 + 1
                        if tipType == "50":
                            tip50 = tip50 + 1

            # calcul volume/component
            for j in range(1,13):
                component = getComponent(Plates_sheet, plate[0], j)
                if component[1] != "":
                    concentration = getConcentration(Plates_sheet, plate[0], component[0])
                    volumes = getVolumes(component[3], plate[3], concentration)
                    # get needed tips
                    tipType = getOneTipType(volumes)
                    aspTotVol = [0, 0, 0, 0, 0, 0, 0, 0]
                    for i in range(8):
                        for col in range(12):
                            aspTotVol[i] = aspTotVol[i] + volumes[col * 8 + i]
                        if aspTotVol[i] != 0:
                            if tipType == "1000":
                                tip1000 = tip1000 + 1
                            if tipType == "300":
                                tip300 = tip300 + 1
                            if tipType == "50":
                                tip50 = tip50 + 1
    neededTips[0] = tip1000
    neededTips[1] = tip300
    neededTips[2] = tip50

    return neededTips

def writeNeededTip(WL_neededTip,neededTip):
    WL_neededTip.write("tip1000" + "\t" + "tip300" + "\t" + "tip50" + "\n")
    WL_neededTip.write(str(neededTip[0]) + "\t" + str(neededTip[1]) + "\t" + str(neededTip[2]))

if __name__ == "__main__":
    Plates_sheet = getExcelSheet(path)

    neededTips=getNeededTips(Plates_sheet)
    print("Tip 1000: " + str(neededTips[0]))
    print("Tip 300: " + str(neededTips[1]))
    print("Tip 50: " + str(neededTips[2]))
    WL_neededTip = open(WLPath, "w")
    writeNeededTip(WL_neededTip,neededTips)





