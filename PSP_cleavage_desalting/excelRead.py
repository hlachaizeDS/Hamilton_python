import xlrd
path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Synthesis_PSP\Hamilton_control_synthesis_PSP.xlsx'

class DSparameters():
    def __init__(self,*args, **kwargs):
        self.THvol1 = 50
        self.THvol2 = 25
        self.shakingTime = 10
        self.transferVol1 = 55
        self.transferVol2 = 55
        self.endoVmixVol = 50
        self.cleavageTime = 1800
        self.bioshakeCleavageStir = 1250
        self.bioshakeCleavageTemp = 37
        self.isopropVol = 375
        self.isopropIncubTime = 180
        self.isopropMixTransferVol = 500
        self.desaltingVacuumTime = 25
        self.ethanolVol = 600
        self.ethanolDryingTime = 900

    def describe(self):
        s=self
        describe_list=["THvol1=","THvol2=","shakingTime=","transferVol1=", "transferVol2=","endoVmixVol=", "cleavageTime=", "bioshakeCleavageStir=", "bioshakeCleavageTemp=", "isopropVol=", "isopropIncubTime=", "isopropMixTransferVol=", "desaltingVacuumTime=", "ethanolVol=", "ethanolDryingTime="]
        children_list=[s.THvol1, s.THvol2, s.shakingTime, s.transferVol1, s.transferVol2, s.endoVmixVol, s.cleavageTime, s.bioshakeCleavageStir, s.bioshakeCleavageTemp, s.isopropVol, s.isopropIncubTime, s.isopropMixTransferVol, s.desaltingVacuumTime, s.ethanolVol, s.ethanolDryingTime]

        for i in range(len(children_list)):
            print(describe_list[i] + str(children_list[i]))

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
    Returns all the wells that have at least one addition of nucleotide during the run
    :param synthesis_sheet
    :return usedWells (arr of int) array of well IDs
    """

    usedWells = []
    sequenceLayout_indexes = findIndexes("Sequence layout", synthesis_sheet)
    well = 1
    for col in range(12):
        for row in range(8):
            sequence = synthesis_sheet.cell_value(sequenceLayout_indexes[0] + 3 + row, sequenceLayout_indexes[1] + 1 + col)
            if sequence != '':
                usedWells.append(well)
            well += 1

    return usedWells

def getDSparameters(synthesis_sheet):
    """
    Returns all the cleavage and desalting parameters (volumes, incubation time...)
    :param synthesis_sheet
    :return parameters (arr)
    """
    parameters=[]

    s = DSparameters

    THvol1Row = findIndexes("TH1 vol 1", synthesis_sheet)[0]
    s.THvol1 = synthesis_sheet.cell_value(THvol1Row, 1)

    THvol2Row = findIndexes("TH1 vol 2", synthesis_sheet)[0]
    s.THvol2 = synthesis_sheet.cell_value(THvol2Row, 1)

    shakingTimeRow = findIndexes("Pre-transfer shaking time", synthesis_sheet)[0]
    s.shakingTime = synthesis_sheet.cell_value(shakingTimeRow, 1)

    transferVol1Row = findIndexes("Transfer vol 1", synthesis_sheet)[0]
    s.transferVol1 = synthesis_sheet.cell_value(transferVol1Row, 1)

    transferVol2Row = findIndexes("Transfer vol 2", synthesis_sheet)[0]
    s.transferVol2 = synthesis_sheet.cell_value(transferVol2Row, 1)

    endoVmixVolRow = findIndexes("EndoV mix volume", synthesis_sheet)[0]
    s.endoVmixVol = synthesis_sheet.cell_value(endoVmixVolRow, 1)

    cleavageTimeRow = findIndexes("Cleavage time", synthesis_sheet)[0]
    s.cleavageTime = synthesis_sheet.cell_value(cleavageTimeRow, 1)

    cleavageStirRow = findIndexes("Bioshake cleavage stir", synthesis_sheet)[0]
    s.bioshakeCleavageStir = synthesis_sheet.cell_value(cleavageStirRow, 1)

    cleavageTempRow = findIndexes("Bioshake cleavage temp", synthesis_sheet)[0]
    s.bioshakeCleavageTemp = synthesis_sheet.cell_value(cleavageTempRow, 1)

    isopropVolRow = findIndexes("Isopropanol volume", synthesis_sheet)[0]
    s.isopropVol = synthesis_sheet.cell_value(isopropVolRow, 1)

    isopropIncubTimeRow = findIndexes("Mix incubation time", synthesis_sheet)[0]
    s.isopropIncubTime = synthesis_sheet.cell_value(isopropIncubTimeRow, 1)

    isopropMixTransferVolRow = findIndexes("Isop mix transfer volume", synthesis_sheet)[0]
    s.isopropMixTransferVol = synthesis_sheet.cell_value(isopropMixTransferVolRow, 1)

    desaltingVacuumTimeRow = findIndexes("Desalting vacuum time", synthesis_sheet)[0]
    s.desaltingVacuumTime = synthesis_sheet.cell_value(desaltingVacuumTimeRow, 1)

    ethanolVolRow = findIndexes("Ethanol wash volume", synthesis_sheet)[0]
    s.ethanolVol = synthesis_sheet.cell_value(ethanolVolRow, 1)

    ethanolDryingTimeRow = findIndexes("Ethanol drying time", synthesis_sheet)[0]
    s.ethanolDryingTime = synthesis_sheet.cell_value(ethanolDryingTimeRow, 1)

    parameters.append(s)

    return parameters


def findIndexes(eltToFind,synthesis_sheet):
    """
    Find in an excel sheet the indexes of the cell containing the string 'eltToFind'
    :param eltToFind: a string to find in the excel file
    :param synthesis_sheet
    :return (row,col)
    """

    for row in range(synthesis_sheet.nrows):
        for col in range(synthesis_sheet.ncols):
            if synthesis_sheet.cell_value(row,col)==eltToFind:
                return (row,col)


if __name__ == "__main__":

    synthesis_sheet=getExcelSheet(path)
    print(getUsedWells(synthesis_sheet))
    parameters=getDSparameters(synthesis_sheet)