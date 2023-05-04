'''
DNAsynthesis
Generate a worklist textControllerFile with all cycle parameters synthesis
Script: Ludivine Profit
Last update: 2020/10/22
'''

from excelRead import*
from WLwrite import *
from cycleRead import *

path = r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\Hamilton_control_synthesis_PSP.xlsx'
worklistPath=r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\WL_DNAsynthesis.txt'

path2 = r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\Cycle.txt'

#Extract number of the first cycle
cycle=int(getCycle(path2))
print('First cycle=' + str(cycle))

#Get back excel synthesis sheet
synthesis_sheet=getExcelSheet(path)

#Extract sequences
sequences=getSequences(synthesis_sheet)
usedWells = getUsedWells(sequences)
print("used wells =")
print(usedWells)

#Extract steps of synthesis
steps=getSteps(synthesis_sheet)

#opening worklist file
WLFile = open(worklistPath, "w")
nucleo_arrays=splitSequences(sequences,cycle)

# extract synthesis format 96 vs 384:
synthesisFormat_96_Boolean = getWellPlateSize(getExcelSheet(path))

# Write column names
WLFile.write("stepName" + "\t" + "PipetType" + "\t" + "IncubTime" + "\t" + "FlushOutTime" + "\t" + "Repeat" + "\t" + "FromLabware" + "\t" + "ToLabware" + "\t" + "LiquidClass" + "\t" + "TipLabware" + "\t" + "TipColumn" + "\t" + "AspirateVol" + "\t" + "AspirateMask" + "\t" + "DispVol" + "\t" + "TipMask" + "\n")

#First wash if first cycle
if cycle == 1:
    writeStep(steps[len(steps)-1], WLFile, nucleo_arrays,usedWells)

#dispenseMode: 0 = 8-channels / 1 = 96-head
dispenseMode = 0

#fill worklist
for step in steps:
    if step.stepName != 0 and step.stepName != "":
        if cycle >= step.changeAtCycle:
            step.fromLabware = step.fromLabware2
        if step.fromLabware == "plate1 to plate4":
            dispenseMode = 1
            plateOrder = getPlateOrder(synthesis_sheet)
            deck_position=[]
            tip_position=[]
            deck_position = ["plate"+ str(j) for j in plateOrder]
            tip_position = ["Tips_300_" + str(j) for j in plateOrder]
            step.fromLabware = deck_position[cycle - 1]
            step.TipLabware = tip_position[cycle - 1]
        writeStep(step,WLFile,nucleo_arrays,usedWells)

#we carry on with next cycle or we end the loop (cycle=0)
isLastCycle = 0
if dispenseMode == 0:
    nucleo_arrays_nextcycle = splitSequences(sequences,cycle+1)
    if len(nucleo_arrays_nextcycle[0]) == len(sequences):
        isLastCycle = 1
else:
    if len(plateOrder) == cycle:
        isLastCycle = 1

if isLastCycle == 1:
    # last wash
    steps[len(steps) - 1].FlushOutTime = 0

    if synthesisFormat_96_Boolean:
        steps[len(steps) - 1].Volume = 60
    else:
        steps[len(steps) - 1].Volume = 25

    writeStep(steps[len(steps) - 1], WLFile, nucleo_arrays,usedWells)
    cycle=0
else:
    cycle=cycle+1

WLFile.close()

print('Current cycle=' + str(cycle))

#Write current cycle in Cycle.txt
writeCycle(path2,cycle)




