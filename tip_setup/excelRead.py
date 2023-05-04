import xlrd
path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Synthesis_PSP\Hamilton_control_synthesis_PSP.xlsx'

import math

def getExcelSheet(path):
    """
    Returns the first sheet of the excel at the path
    :param path:
    :return:
    """
    wb = xlrd.open_workbook(path)
    synthesis_sheet = wb.sheet_by_index(0)
    return synthesis_sheet

def getUsedWells(synthesis_sheet):
    """
    Returns all the wells that have at least one addition of nucleotide in the run
    :param sequences:
    :return:
    """
    sequenceLayout_indexes = findIndexes("Sequence layout", synthesis_sheet)
    usedWells = []
    well=1
    for col in range(12):
        for row in range(8):
            value = synthesis_sheet.cell_value(sequenceLayout_indexes[0] + 3 + row, sequenceLayout_indexes[1] + 1 + col)
            if value != '':
                usedWells.append(well)
            well += 1
    return usedWells

def getLoopNbr():
    loopNbr=math.ceil(len(usedWells)/8)
    return loopNbr

def getLastTipMask():
    lastTipMask=""
    rest=(len(usedWells))%8
    if rest == 1:
        lastTipMask = "10000000"
    if rest == 2:
        lastTipMask = "11000000"
    if rest == 3:
        lastTipMask = "11100000"
    if rest == 4:
        lastTipMask = "11110000"
    if rest == 5:
        lastTipMask = "11111000"
    if rest== 6:
        lastTipMask = "11111100"
    if rest == 7:
        lastTipMask = "11111110"
    if rest == 0:
        lastTipMask = "11111111"
    return lastTipMask

def findIndexes(eltToFind,synthesis_sheet):
    """
    Find in an excel sheet the indexes of the cell containing the string 'eltToFind'
    :param eltToFind: a string to find in the excel file
    :param synthesis_sheet:
    :return:
    """

    for row in range(synthesis_sheet.nrows):
        for col in range(synthesis_sheet.ncols):
            if synthesis_sheet.cell_value(row,col)==eltToFind:
                return (row,col)


synthesis_sheet = getExcelSheet(path)
usedWells = getUsedWells(synthesis_sheet)
loopNbr=getLoopNbr()
lastTipMask=getLastTipMask()
print((len(usedWells))%8)
print(lastTipMask)
print(usedWells)
print(loopNbr)




