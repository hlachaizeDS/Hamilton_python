from WLwrite import *
from cycleRead import *

path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Hamilton_control_synthesis_PSP.xlsx'
worklistPath=r'C:\Users\Hamilton\Desktop\HAMILTON_control\textControllerFile.txt'

path2 = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Cycle.txt'

#Extract number of the first cycle
cycle=int(getCycle(path2))
print('First cycle=' + str(cycle))

#Get back excel synthesis sheet
synthesis_sheet=getExcelSheet(path)

#Extract sequences
sequences=getSequences(synthesis_sheet)

#Extract steps of synthesis
steps=getSteps(synthesis_sheet)

#Get 96-head premix dispense script
headScript = get96headScript(synthesis_sheet)

#opening worklist file
WLFile = open(worklistPath, "w")
nucleo_arrays=splitSequences(sequences,cycle)

# Write column names (Script variables)
WLFile.write("stepName" + "\t" + "PipetType" + "\t" + "IncubTime" + "\t" + "FlushOutTime" + "\t" + "Repeat" + "\t" + "FromLabware" + "\t" + "ToLabware" + "\t" + "LiquidClass" + "\t" + "TipLabware" + "\t" + "TipColumn" + "\t" + "AspirateVol" + "\t" + "AspirateMask" + "\t" + "DispVol" + "\t" + "TipMask" + "\n")


#First wash if first cycle
if cycle == 1:
    writeStep(steps[len(steps)-1], WLFile, nucleo_arrays)

#fill worklist
for step in steps:
    if cycle >= step.changeAtCycle:
        step.fromLabware=step.fromLabware2
    if headScript == 1:
        plateOrder = getPlateOrder(synthesis_sheet)
        print(plateOrder)
        if step.fromLabware == "Step2":
             deck_position=[]
             tip_position=[]
             deck_position = ["Step"+ str(j+1) for j in plateOrder]
             tip_position = ["Tips_300_" + str(j+1) for j in plateOrder]
             step.fromLabware=deck_position[cycle - 1]
             step.TipLabware=tip_position[cycle - 1]
    writeStep(step,WLFile,nucleo_arrays)

#Last wash
nucleo_arrays_nextcycle = splitSequences(sequences,cycle+1)
if len(nucleo_arrays_nextcycle[0]) == len(sequences):
    steps[len(steps) - 1].FlushOutTime=0
    steps[len(steps) - 1].Volume = 50
    writeStep(steps[len(steps)-1], WLFile, nucleo_arrays)

WLFile.close()



#we carry on with next cycle or we end the loop (cycle=0)
nucleo_arrays_nextcycle = splitSequences(sequences,cycle+1)
if len(nucleo_arrays_nextcycle[0]) == len(sequences):
    cycle=0
else:
    cycle=cycle+1

print('Current cycle=' + str(cycle))

#Write current cycle in Cycle.txt
writeCycle(path2,cycle)




