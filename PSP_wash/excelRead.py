import xlrd
path = r'C:\Users\Martin\OneDrive - DNA Script\Documents\H_Simu\Hamilton_control_synthesis_PSP.xlsx'



class PSPstep():
    def __init__(self,*args, **kwargs):
        self.stepNumber=0
        self.stepName="water"
        self.fromLabware="water"
        self.liquidClass="Water"
        self.volume=50
        self.tipLabware="water"
        self.incubationTime=30
        self.flushOutTime=20
        self.repeats=1


    def describe(self):
        s=self
        describe_list=["stepNumber=","stepName=","fromLabware=", "liquidClass=","volume=", "tipLabware=", "incubationTime=", "flushOutTime=", "repeats="]
        children_list=[s.stepNumber, s.stepName, s.fromLabware, s.liquidClass, s.volume, s.tipLabware, s.incubationTime, s.flushOutTime, s.repeats]

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


def getSteps(synthesis_sheet):
    """
    Returns wash step parameters from synthesis_sheet
    :param synthesis_sheet
    :return steps
    """

    steps=[]

    step_number_indexes=findIndexes("PSP step number",synthesis_sheet)

    for step in range(8):
        stepColumn=step_number_indexes[1]+1+step
        stepName_indexes=findIndexes("PSP step name",synthesis_sheet)
        stepName=synthesis_sheet.cell_value(stepName_indexes[0],stepColumn)

        if (stepName!= 0.0):
            s=PSPstep()
            stepNumberRow = findIndexes("PSP step number", synthesis_sheet)[0]
            s.stepNumber = int(synthesis_sheet.cell_value(stepNumberRow, stepColumn))
            stepNameRow = findIndexes("PSP step name", synthesis_sheet)[0]
            s.stepName = synthesis_sheet.cell_value(stepNameRow, stepColumn)
            fromLabwareRow = findIndexes("PSP from labware", synthesis_sheet)[0]
            s.fromLabware = synthesis_sheet.cell_value(fromLabwareRow, stepColumn)

            liquidClassRow = findIndexes("PSP liquid class", synthesis_sheet)[0]
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "Water":
                s.liquidClass="HighVolume_Water_DispenseJet_Part"
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "Viscous":
                s.liquidClass="HighVolume_Premix_DispenseJet_Part"


            volumeRow = findIndexes("PSP volume (µL)", synthesis_sheet)[0]
            s.volume = int(synthesis_sheet.cell_value(volumeRow,stepColumn))
            tipLabwareRow = findIndexes("PSP tips", synthesis_sheet)[0]
            s.tipLabware = synthesis_sheet.cell_value(tipLabwareRow, stepColumn)
            incubationTimeRow = findIndexes("PSP incubation time (s)", synthesis_sheet)[0]
            s.incubationTime = int(synthesis_sheet.cell_value(incubationTimeRow, stepColumn))
            flushOutTimeRow = findIndexes("PSP flushOut time (s)", synthesis_sheet)[0]
            s.flushOutTime = int(synthesis_sheet.cell_value(flushOutTimeRow, stepColumn))
            repeatsRow = findIndexes("PSP number of repeats", synthesis_sheet)[0]
            s.repeats = int(synthesis_sheet.cell_value(repeatsRow, stepColumn))

            steps.append(s)

    return steps


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
    steps=getSteps(synthesis_sheet)
    steps[0].describe()