import xlrd
path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\Hamilton_control_synthesis_PSP.xlsx'

class SynthesisStep():
    def __init__(self,*args, **kwargs):
        self.stepNumber=0
        self.pipetType="premix"
        self.fromLabware="A_nucs"
        self.stepName="Mix1"
        self.LiquidClass="Water"
        self.Volume=50
        self.TipLabware="Premix_Tips"
        self.incubationTime=4*60
        self.repeats=1
        self.every=1
        self.changeAtCycle=300
        self.FlushOutTime=0
        self.fromLabware2="extra"


    def describe(self):
        s=self
        describe_list=["stepNumber=","pipetType=","fromLabware=", "stepName=", "LiquidClass=","Volume=", "TipLabware=", "incubationTime=", "FlushOutTime=", "repeats=", "every=", "changeAtCycle=", "fromLabware2="]
        children_list=[s.stepNumber, s.pipetType, s.fromLabware, s.stepName, s.LiquidClass, s.Volume, s.TipLabware, s.incubationTime, s.FlushOutTime, s.repeats, s.every, s.changeAtCycle, s.fromLabware2]

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

def getPlateOrder(synthesis_sheet):
    """
        Reads the first sheet of the Quartet Control file and returns plateOrder in an array
        :param synthesis_sheet: an excel sheet
        :return:
        """

    plateOrder = []
    plateOrder_indexes = findIndexes("Plate order", synthesis_sheet)
    for cycle in range(60):
        plate = synthesis_sheet.cell_value(plateOrder_indexes[0],plateOrder_indexes[1]+1+cycle)
        if plate != "":
                plateOrder.append(int(plate))
    return plateOrder

def getSequences(synthesis_sheet):
    """
    Reads the first sheet of the Quartet Control file and returns all the sequences in it in an array
    :param synthesis_sheet: an excel sheet
    :return:
    """

    sequences=[]
    well=1
    for col in range(12):
        for row in range(8):
            value=synthesis_sheet.cell_value(5+row,1+col)
            if value!='':
                sequences.append((well,value))
            well+=1

    return sequences

def get96headScript(synthesis_sheet):
    headScript_indexes = findIndexes("96-head script", synthesis_sheet)
    headScript = synthesis_sheet.cell_value(headScript_indexes[0], headScript_indexes[1] + 1)
    return headScript

def getSteps(synthesis_sheet):

    steps=[]

    step_number_indexes=findIndexes("Step number",synthesis_sheet)

    variables=["Step number","Pipet type","Deck position","Reagent","Liquid class","Volume (µL)","Tips","Incubation time (s)", "FlushOutTime (s)", "Number of repeats","Every x cycles","Change at cycle x","Deck position 2"]

    for step in range(8):
        stepColumn=step_number_indexes[1]+1+step
        stepName_indexes=findIndexes("Reagent",synthesis_sheet)
        stepName=synthesis_sheet.cell_value(stepName_indexes[0],stepColumn)

        if (stepName!= 0.0):
            s=SynthesisStep()
            newStepParameters=["s.stepNumber","s.pipetType","s.fromLabware","s.stepName","s.LiquidClass","s.Volume","s.TipLabware","s.incubationTime", "s.FlushOutTime","s.repeats","s.every","s.changeAtCycle", "s.fromLabware2"]

            stepNumberRow=findIndexes("Step number",synthesis_sheet)[0]
            s.stepNumber=int(synthesis_sheet.cell_value(stepNumberRow,stepColumn))
            pipetTypeRow = findIndexes("Pipet type", synthesis_sheet)[0]
            s.pipetType = int(synthesis_sheet.cell_value(pipetTypeRow, stepColumn))
            fromLabwareRow = findIndexes("Deck position", synthesis_sheet)[0]
            s.fromLabware = synthesis_sheet.cell_value(fromLabwareRow, stepColumn)
            stepNameRow = findIndexes("Reagent", synthesis_sheet)[0]
            s.stepName = synthesis_sheet.cell_value(stepNameRow, stepColumn)

            liquidClassRow = findIndexes("Liquid class", synthesis_sheet)[0]
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "DMSO":
                s.LiquidClass="StandardVolume_96COREHead1000ul_Water_DispenseJet_Empty"
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "Water":
                s.LiquidClass="StandardVolume_96COREHead1000ul_Water_DispenseJet_Empty"
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "WB":
                s.LiquidClass="StandardVolume_96COREHead1000ul_BB_DispenseJet_Empty"
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "DB":
                s.LiquidClass="StandardVolume_96COREHead1000ul_DB_DispenseJet_Empty"
            if synthesis_sheet.cell_value(liquidClassRow, stepColumn) == "Premix":
                s.LiquidClass="StandardVolume_96COREHead1000ul_Supernantant_DispenseJet_Empty"


            volumeRow = findIndexes("Volume (µL)", synthesis_sheet)[0]
            s.Volume = int(synthesis_sheet.cell_value(volumeRow,stepColumn))
            TipLabwareRow = findIndexes("Tips", synthesis_sheet)[0]
            s.TipLabware = synthesis_sheet.cell_value(TipLabwareRow, stepColumn)
            incubationTimeRow = findIndexes("Incubation time (s)", synthesis_sheet)[0]
            s.incubationTime = int(synthesis_sheet.cell_value(incubationTimeRow, stepColumn))
            FlushOutTimeRow = findIndexes("FlushOut time (s)", synthesis_sheet)[0]
            s.FlushOutTime = int(synthesis_sheet.cell_value(FlushOutTimeRow, stepColumn))
            repeatsRow = findIndexes("Number of repeats", synthesis_sheet)[0]
            s.repeats = int(synthesis_sheet.cell_value(repeatsRow, stepColumn))
            #everyRow = findIndexes("Every x cycles", synthesis_sheet)[0]
            #s.every = int(synthesis_sheet.cell_value(everyRow, stepColumn))
            changeAtCycleRow = findIndexes("Change at cycle x", synthesis_sheet)[0]
            s.changeAtCycle = int(synthesis_sheet.cell_value(changeAtCycleRow, stepColumn))
            fromLabware2Row = findIndexes("Deck position 2", synthesis_sheet)[0]
            s.fromLabware2 = synthesis_sheet.cell_value(fromLabware2Row, stepColumn)

            steps.append(s)

    return steps

def splitSequences(sequences,cycle):
    """
    Split sequences depending on the cycle we're at, and returns an array of 5 arrays containing the wells that should
    receive each nucleotide
    :param sequences:
    :param cycle:
    :return:
    """

    ended_wells = []
    A_wells=[]
    C_wells=[]
    G_wells=[]
    T_wells=[]
    M_wells=[]
    N_wells = []
    O_wells = []
    P_wells = []
    W_wells = []
    X_wells = []
    Y_wells = []
    Z_wells = []
    U_wells = []

    nucleos=['A','C','G','T','M','N','O','P','W','X','Y','Z','U']
    nucleo_arrays=[ended_wells,A_wells,C_wells,G_wells,T_wells,M_wells,N_wells,O_wells,P_wells,W_wells,X_wells,Y_wells,Z_wells,U_wells]

    for nucleo in range(1,13+1):
        for sample in range(len(sequences)):
            if (cycle<=len(sequences[sample][1]) and sequences[sample][1][cycle-1]==nucleos[nucleo-1]):
                nucleo_arrays[nucleo].append(sequences[sample][0])

    for sample in range(len(sequences)):
        if cycle > len(sequences[sample][1]):
            ended_wells.append(sequences[sample][0])

    return nucleo_arrays

def getUsedWells(sequences):
    """
    Returns all the wells that have at least one addition of nucleotide in the run
    :param sequences:
    :return:
    """

    usedWells=[]
    for sample in sequences:
        usedWells.append(sample[0])
    return usedWells

def getActiveWells(sequences,cycle):
    """
    Returns all the wells that are still synthesizing (not the finished ones)
    :param sequences:
    :param cycle:
    :return:
    """
    usedWells=getUsedWells(sequences)
    ended_wells=splitSequences(sequences,cycle)[0]
    activeWells=[]

    for well in usedWells:
        if well not in ended_wells:
            activeWells.append(well)

    return activeWells

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

'''
def getParameters(synthesis_sheet):
    param_indexes=findIndexes('Parameter',synthesis_sheet)
    for row in range(param_indexes[0]+1,synthesis_sheet.nrows):
        code=synthesis_sheet.cell_value(row,1) + '=' + str(synthesis_sheet.cell_value(row,3))
        #print(code)
        exec(code,globals())
'''

if __name__ == "__main__":

    synthesis_sheet=getExcelSheet(path)
    sequences=getSequences(synthesis_sheet)
    print(sequences)
    nucleo_arrays=splitSequences(sequences,5)
    print(nucleo_arrays[0])
    print(nucleo_arrays[1])
    print(nucleo_arrays[2])
    print(nucleo_arrays[3])
    print(nucleo_arrays[4])
    print(nucleo_arrays[5])
    print(nucleo_arrays[6])
    print(nucleo_arrays[7])
    print(nucleo_arrays[8])
    print(nucleo_arrays[9])
    print(nucleo_arrays[10])
    print(nucleo_arrays[11])
    print(nucleo_arrays[12])
    print(nucleo_arrays[13])
    #params=getParameters(synthesis_sheet)
    print(getUsedWells(sequences))

    steps=getSteps(synthesis_sheet)
    steps[0].describe()