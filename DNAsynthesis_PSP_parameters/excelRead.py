import xlrd
import datetime

# path of excel control file:
path = r'Hamilton_control_synthesis_PSP.xlsx'

def getExcelSheet(path):
    """
    Returns the first sheet of the excel at the path
    :param path:
    :return:
    """
    wb = xlrd.open_workbook(path)
    synthesis_sheet = wb.sheet_by_index(0)
    return synthesis_sheet

def getRunParameters(synthesis_sheet):
    """
    Returns synthesis run parameters
    :param synthesis_sheet
    :return runParameters (arr) array of 3 bln corresponding to synthesis, PSP washes and cleavage/desalting steps
    """
    runParameters=[0,0,0]

    # perform synthesis
    performSynthesisIndex = findIndexes("Perform synthesis", synthesis_sheet)
    performSynthesis = synthesis_sheet.cell_value(performSynthesisIndex[0], performSynthesisIndex[1]+1)
    if performSynthesis == "":
        performSynthesis = 0
    else:
        performSynthesis = int(performSynthesis)
    runParameters[0] = performSynthesis

    # perform PSP washes
    performPSPwashesIndex = findIndexes("Perform PSP washes", synthesis_sheet)
    performPSPwashes = synthesis_sheet.cell_value(performPSPwashesIndex[0], performPSPwashesIndex[1]+1)
    if performPSPwashes == "":
        performPSPwashes = 0
    else:
        performPSPwashes = int(performPSPwashes)
    runParameters[1] = performPSPwashes

    # perform cleavage and desalting
    performCleavageDesaltingIndex = findIndexes("Perform cleavage and desalting", synthesis_sheet)
    performCleavageDesalting = synthesis_sheet.cell_value(performCleavageDesaltingIndex[0], performCleavageDesaltingIndex[1]+1)
    if performCleavageDesalting == "":
        performCleavageDesalting = 0
    else:
        performCleavageDesalting = int(performCleavageDesalting)
    runParameters[2] = performCleavageDesalting

    return runParameters

def getPSPdate(synthesis_sheet):
    """
    Returns starting hour and date of cleavage and desalting
    :param synthesis_sheet
    :return PSPdate (arr) array of 5 int: year, month, day (day after synthesis day), hour, min
    """
    PSPdate = [0, 0, 0, 0, 0]

    # date (day after synthesis)
    synthesisDate = datetime.date.today()
    PSPdate[0] = synthesisDate.year
    PSPdate[1] = synthesisDate.month
    PSPdate[2] = synthesisDate.day + 1

    # starting hour
    startingHourIndex = findIndexes("Start at:", synthesis_sheet)
    startingHour = synthesis_sheet.cell_value(startingHourIndex[0], startingHourIndex[1] + 1)
    if startingHour == "":
        startingHour = 0
    else:
        startingHour = int(startingHour)
    PSPdate[3] = startingHour
    startingMinute = synthesis_sheet.cell_value(startingHourIndex[0], startingHourIndex[1] + 2)
    if startingMinute == "":
        startingMinute = 0
    else:
        startingMinute = int(startingHour)
    PSPdate[4] = startingMinute

    return PSPdate

def findIndexes(eltToFind,synthesis_sheet):
    """
    Find in an excel sheet the indexes of the cell containing the string 'eltToFind'
    :param eltToFind: a string to find in the excel file
    :param synthesis_sheet:
    :return (row, col)
    """

    for row in range(synthesis_sheet.nrows):
        for col in range(synthesis_sheet.ncols):
            if synthesis_sheet.cell_value(row,col)==eltToFind:
                return (row,col)

if __name__ == "__main__":

    synthesis_sheet=getExcelSheet(path)
    runParameters = getRunParameters(synthesis_sheet)
    PSPdate = getPSPdate()
    print(runParameters)
    print(PSPdate)
