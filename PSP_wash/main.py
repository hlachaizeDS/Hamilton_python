'''
PSP_wash
Generate a worklist WL_PSP_wash with aspirate/dispense parameters for PSP washes
Script: Ludivine Profit
Last update: 2020/10/22
'''

from WLwrite import *
from excelRead import*
from simpleFunctions import*

path = r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\Hamilton_control_synthesis_PSP.xlsx'
worklistPath=r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\WL_PSP_wash.txt'

#Get back excel synthesis sheet
synthesis_sheet=getExcelSheet(path)

#Extract steps of synthesis
steps=getSteps(synthesis_sheet)

#Extract usedWells
usedWells=getUsedWells(synthesis_sheet)

#opening worklist file
WL_PSP_washes = open(worklistPath, "w")

#Write column names (Script variables)
writeVariableName(WL_PSP_washes)


#fill worklist
for step in steps:
    volumes=getVolumes(usedWells,step.volume)
    aspVolDispCol = getAspVolDispCol(volumes)
    aspVolVol = aspVolDispCol[0]
    numberOfAsp = getNumberOfAsp(aspVolVol)
    dispColCol = aspVolDispCol[1]
    tipMaskStr = getTipMask(volumes)
    tipColumn=getTipColumn(step.tipLabware)

    for x in range (step.repeats):
        j = 0
        for aspVol in aspVolVol:
            aspVolStr = getAspVolStr(aspVol)
            aspMask = getAspDispMask(aspVol)
            aspMaskStr = getAspDispMaskStr(aspMask)
            if aspMaskStr != "00000000":
                aspDispMode = "0"
                writeVariable(WL_PSP_washes, step, aspDispMode, step.fromLabware, tipColumn, tipMaskStr, aspVolStr, aspMaskStr, "seq", numberOfAsp)
                dispCol = dispColCol[j]
                for column in dispCol:
                    dispVol = getDispVol(volumes, column)
                    dispVolStr = getDispVolStr(dispVol)
                    dispMask = getAspDispMask(dispVol)
                    dispMaskStr = getAspDispMaskStr(dispMask)
                    dispSeqStr = getDispSeqStr(usedWells, column)
                    if dispMaskStr != "00000000":
                        aspDispMode = "1"
                        writeVariable(WL_PSP_washes, step, aspDispMode, "filter_plate_384", tipColumn, tipMaskStr, dispVolStr,dispMaskStr, dispSeqStr, numberOfAsp)
            j = j + 1

#write a last lane with mode = 0
WL_PSP_washes.write("0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0" + "\t" + "0")


WL_PSP_washes.close()


