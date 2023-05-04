import xlrd

path = r'C:\Users\Hamilton\Desktop\HAMILTON_control\plate_preparation\Plate_preparation.xlsx'

def getExcelSheet(path):
    """
    Returns the first sheet of the excel at the path
    :param path of the Excel you want to read
    :return sheet
    """
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    return sheet

def getPlate(sheet,i):
    """
    Reads an excel sheet and returns an array with plate i information: plate index, plate name, plate position on the deck, final volume
    :param sheet (excel sheet)
    :param i (int): plate number
    :return plate (arr): [plateIndex, plateName, platePosition, finalVol]
    """
    col = (i-1) * 15
    plateIndex = [findRowIndex("Plate ID", sheet, col), col]
    plateNameIndex = [plateIndex[0], plateIndex[1] + 1]
    plateName = sheet.cell_value(plateNameIndex[0], plateNameIndex[1])
    platePositionIndex = [1 + plateIndex[0], 1 + plateIndex[1]]
    platePosition = sheet.cell_value(platePositionIndex[0], platePositionIndex[1])
    finalVolIndex = [2 + plateIndex[0], 1 + plateIndex[1]]
    finalVol = sheet.cell_value(finalVolIndex[0], finalVolIndex[1])
    plate = [plateIndex, plateName, platePosition, finalVol]
    return plate

def getComponent(sheet,plateIndex,j):
    """
    Reads an excel sheet and Returns an array with component j of plate i information: component index, component name, component position on the deck, component stock concentration
    :param sheet (excel sheet)
    :param plateIndex (arr): excel cell indexes of the plate i
    :param j (int): component number
    :return component (arr): [componentIndex,componentName,componentPosition,stockConc]
    """

    row = 14 * (j-1) + 4
    componentIndex=[plateIndex[0]+(row),plateIndex[1]]
    componentNameIndex=[componentIndex[0],componentIndex[1]+1]
    componentName=str(sheet.cell_value(componentNameIndex[0],componentNameIndex[1]))
    componentPositionIndex=[componentIndex[0]+1,componentIndex[1]+1]
    componentPosition = sheet.cell_value(componentPositionIndex[0], componentPositionIndex[1])
    componentPosition = str(componentPosition)
    stockConcIndex = [componentIndex[0]+2,componentIndex[1]+1]
    stockConc=sheet.cell_value(stockConcIndex[0],stockConcIndex[1])
    component = [componentIndex,componentName,componentPosition,stockConc]
    return component

def getConcentration(sheet, plateIndex, componentIndex):
    """
    Reads an excel sheet and Returns an array of 96 concentrations
    :param sheet (excel sheet)
    :param plateIndex (arr): excel cell indexes of the plate i
    :param componentIndex (arr): excel cell indexes of the component j
    :return concentration (arr): 96 concentrations
    """

    concentrationIndex=[componentIndex[0]+5,plateIndex[1]+2]
    concentration=[]
    for col in range (12):
        for row in range (8):
            if sheet.cell_value(concentrationIndex[0]+row,concentrationIndex[1]+col) == "":
                concentration.append(0)
            else:
                concentration.append(sheet.cell_value(concentrationIndex[0]+row,concentrationIndex[1]+col))
    return concentration

def findRowIndex(eltToFind,sheet,col):
    """
    Find in an excel sheet the row index of the cell of column col containing the string 'eltToFind'
    :param eltToFind: a string to find in the excel file
    :param sheet: sheet
    :param col: column
    :return row: row index of the cell containing the string 'eltToFind'
    """

    for row in range(sheet.nrows):
        if sheet.cell_value(row,col)==eltToFind:
            return (row)

if __name__ == "__main__":

    Plates_sheet=getExcelSheet(path)
    plate = getPlate(Plates_sheet, 0)
    print(plate)
    component = getComponent(Plates_sheet,plate[0],0)
    print(component)
    print(getConcentration(Plates_sheet,plate[0],component[0]))



