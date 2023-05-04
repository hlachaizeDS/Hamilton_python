'''
DNAsynthesis_PSP_parameters
Generate a worklist WL_PSP_parameters indicating if you want to perform: synthesis - PSP washes - cleavage/desalting (and the starting hour)
Script: Ludivine Profit
Last update: 2020/10/22
'''

from WLwrite import *
from excelRead import*

path = r'Hamilton_control_synthesis_PSP.xlsx'
worklistPath=r'WL_synthesis_PSP_parameters.txt'

# get back excel synthesis sheet
synthesis_sheet=getExcelSheet(path)

# open WL
WL_synthesis_PSP_parameters=open(worklistPath, "w")

# get process parameters
runParameters = getRunParameters(synthesis_sheet)

# get PSP date
PSPdate = getPSPdate(synthesis_sheet)

# write in WL
writeVariableName(WL_synthesis_PSP_parameters)
writeRunParameters(WL_synthesis_PSP_parameters, runParameters, PSPdate)


