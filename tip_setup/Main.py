from WLwrite import *

path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Synthesis_PSP\Hamilton_control_synthesis_PSP.xlsx'
worklistPath=r'C:\Users\Hamilton\Desktop\HAMILTON_control\TipSetUp\TipPrepWL.txt'

#Get back excel synthesis sheet
synthesis_sheet=getExcelSheet(path)

#Extract used wells
UsedWells=getUsedWells(synthesis_sheet)

#opening worklist file
WLFile = open(worklistPath, "w")

# Write column names (Script variables)
writeColumnName(WLFile)

#fill worklist
for i in usedWells:
    writeValue(WLFile,i)

WLFile.close()


