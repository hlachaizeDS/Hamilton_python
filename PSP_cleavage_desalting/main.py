'''
PSP_cleavage_desalting
Generate a worklist WL_PSP_cleavage_desalting with all aspirate/dispense parameters for cleavage and desalting steps
Script: Ludivine Profit
Last update: 2020/10/22
'''

from WLwrite import *
from excelRead import*
from simpleFunctions import*

path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Synthesis_PSP\Hamilton_control_synthesis_PSP.xlsx'
worklistPath1=r'C:\Users\Hamilton\Desktop\HAMILTON_control\Synthesis_PSP\WL_DSparameters.txt'
worklistPath2=r'C:\Users\Hamilton\Desktop\HAMILTON_control\Synthesis_PSP\WL_PSP_cleavage_desalting.txt'

#Get back excel synthesis sheet
synthesis_sheet=getExcelSheet(path)


#Extract excel info
usedWells=getUsedWells(synthesis_sheet)
parameters=getDSparameters(synthesis_sheet)

#opening worklist files
WL_DSparameters = open(worklistPath1, "w")
WL_PSP_cleavage_desalting_V2 = open(worklistPath2, "w")

#Write in WL_DSparameters
WL_DSparameters.write("shakingTime" + "\t" + "transferVol1"+ "\t" + "transferVol2"+ "\t" + "cleavageTime"+ "\t" + "bioshakeCleavageStir" + "\t" + "bioshakeCleavageTemp" + "\t" + "isopropIncubTime" + "\t" + "isopropTransferVol" + "\t" + "desaltingVacuumTime" + "\t" + "ethanolDryngTime"  + "\n")
writeDSparameters(WL_DSparameters,DSparameters)

WL_DSparameters.close()

#Write column names (Script variables)
writeVariableName(WL_PSP_cleavage_desalting_V2)


reagentList=["TH1X", "TH1X", "endoVmix", "isopropanol", "ethanol","ethanol"]
liquidClassList = ["HighVolume_Water_DispenseJet_Part","HighVolume_Water_DispenseJet_Part","HighVolume_Premix_DispenseJet_Part","HighVolume_EtOH_DispenseJet_Part","HighVolume_EtOH_DispenseJet_Part","HighVolume_EtOH_DispenseJet_Part"]
volumeList=[DSparameters.THvol1,DSparameters.THvol2,DSparameters.endoVmixVol,DSparameters.isopropVol, DSparameters.ethanolVol,DSparameters.ethanolVol]
destinationPlateList=["FilterPlate","FilterPlate","cleavagePlate", "cleavagePlate","FilterPlate","FilterPlate"]

pipettingParameters = [reagentList,liquidClassList,volumeList, destinationPlateList]

i=0
for reagent in reagentList:
    volumes=getVolumes(usedWells,volumeList[i])
    aspVolDispCol = getAspVolDispCol(volumes)
    aspVolVol = aspVolDispCol[0]
    numberOfAsp = getNumberOfAsp(aspVolVol)
    dispColCol = aspVolDispCol[1]
    tipMaskStr = getTipMask(volumes)
    tipColumn=getTipColumn(reagent)

    j=0
    for aspVol in aspVolVol:
        aspVolStr = getAspVolStr(aspVol)
        aspMask = getAspDispMask(aspVol)
        aspMaskStr = getAspDispMaskStr(aspMask)
        if aspMaskStr != "00000000":
            aspDispMode = "0"
            labware = pipettingParameters[0][i]
            writeVariable(WL_PSP_cleavage_desalting_V2, i, pipettingParameters, aspDispMode, labware, tipColumn, tipMaskStr, aspVolStr, aspMaskStr, "seq", numberOfAsp)

            dispCol = dispColCol[j]
            for column in dispCol:
                dispVol = getDispVol(volumes, column)
                dispVolStr = getDispVolStr(dispVol)
                dispMask = getAspDispMask(dispVol)
                dispMaskStr = getAspDispMaskStr(dispMask)
                dispSeqStr = getDispSeqStr(usedWells, column)
                if dispMaskStr != "00000000":
                    aspDispMode = "1"
                    labware = pipettingParameters[3][i]
                    writeVariable(WL_PSP_cleavage_desalting_V2, i, pipettingParameters, aspDispMode, labware, tipColumn, tipMaskStr, dispVolStr, dispMaskStr, dispSeqStr, numberOfAsp)
        j=j+1
    i=i+1

#write a last lane to end the loop on Hamilton
WL_PSP_cleavage_desalting_V2.write("O" + "\t" + "O" + "\t" + "O" + "\t" + "O" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0")



WL_PSP_cleavage_desalting_V2.close()