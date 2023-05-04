def getTipColumn(reagent):
    """
    Returns the tip column from Tips_1000_PSP tip box
    :param reagent (str)
    :return tipColumn (int)
    """
    tipColumn=""
    if reagent == "TH1X":
        tipColumn = 3
    if reagent == "endoVmix":
        tipColumn = 4
    if reagent == "isopropanol":
        tipColumn = 5
    if reagent == "ethanol":
        tipColumn = 6
    return tipColumn

def getVolumes(usedWells,volume):
    """
    Returns an array of 96 volumes to be dispensed with 8-channels
    :param usedWells (arr) stock concentration of component i
    :param volume (float) volume/well
    :return volumes (array of float)
    """
    volumes = []
    for i in range(96):
        volumes.append(0)

    for well in usedWells:
        volumes[well - 1] = volume

    return volumes

def getAspVolDispCol(volumes):
    """
    Calculates aspirate volumes of component i and columns of plate j where dispense
    :param volumes (array of float) 96 volumes of component i to be dispensed in plate j
    :return aspVolDispCol array of:
    aspVolVol: array of arrays aspVol = 8 volumes of component i to aspirate (1 volume/channel)
    dispColCol: array of arrays dispCol = columns of the plate j to dispense per aspirate
    """
    # array of arrays of aspirate volumes per component per plate
    aspVolVol = []
    aspVol = [0, 0, 0, 0, 0, 0, 0, 0]
    # array of arrays of column to dispense
    dispColCol = []
    dispCol = []
    aspVolDispCol = []
    # if one volume of aspVol is > 1000: max is true
    max = "false"
    for col in range (12):
            for i in range (8):
                aspVol[i] = aspVol[i] + volumes[col * 8 + i]
                if aspVol[i] > 940:
                    max = "true"
            if max == "true":
                for i in range (8):
                    aspVol[i] = aspVol[i] - volumes[col * 8 + i]
                    #add 10µL of conditioning volume
                    if aspVol[i] != 0:
                        aspVol[i]=aspVol[i]+10
                aspVolVol.append(aspVol.copy())
                dispColCol.append(dispCol.copy())
                dispCol=[]
                for i in range (8):
                    aspVol[i] = volumes[col * 8 + i]
                max = "false"
            if col == 11:
                dispCol.append(col)
                # add 10µL of conditioning volume
                for i in range (8):
                    if aspVol[i] != 0:
                        aspVol[i] = aspVol[i] + 10
                aspVolVol.append(aspVol.copy())
                dispColCol.append(dispCol.copy())
                dispCol = []
            dispCol.append(col)
    aspVolDispCol.append(aspVolVol)
    aspVolDispCol.append(dispColCol)
    return aspVolDispCol

def getAspVolDispCol_wRefill(volumes):
    """
    Calculates aspirate volumes of component i and columns of plate j where dispense
    :param volumes (array of float) 96 volumes of component i to be dispensed in plate j
    :return aspVolDispCol array of:
    aspVolVol: array of arrays aspVol = 8 volumes of component i to aspirate (1 volume/channel)
    dispColCol: array of arrays dispCol = columns of the plate j to dispense per aspirate
    """

    vols=volumes.copy()
    max_vol_per_tip=940

    # array of arrays of aspirate volumes per component per plate
    aspVolVol = []
    # array of arrays of column to dispense
    dispColCol = []
    aspVolDispCol = []

    while vols != [ 0 for i in range(96) ]:
        aspVol = [0, 0, 0, 0, 0, 0, 0, 0]
        dispCol = []
        max_in_one_tip=0
        for col in range(12):
            if max_in_one_tip:
                break
            for i in range(8):
                if aspVol[i] + vols[col * 8 + i] <= max_vol_per_tip:
                    aspVol[i] = aspVol[i] + vols[col * 8 + i]
                    vols[col * 8 + i] = 0
                else:
                    vols[col * 8 + i] = vols[col * 8 + i] - (max_vol_per_tip - aspVol[i])
                    aspVol[i] = max_vol_per_tip
                    max_in_one_tip=1
            dispCol.append(col)
        # add 10µL of conditioning volume
        for i in range(8):
            if aspVol[i] != 0:
                aspVol[i] = aspVol[i] + 10
        aspVolVol.append(aspVol.copy())
        dispColCol.append(dispCol.copy())

    aspVolDispCol.append(aspVolVol)
    aspVolDispCol.append(dispColCol)

    return aspVolDispCol

def getDispSeqStr(wells,column):
    """
    Returns a string of wells to dispense per column
    :param wells (array of int) active wells
    :param column (int)
    :return dispSeqStr (str) number of wells and well IDs
    """
    #dispSeq = well number, wells
    dispSeq=[0]
    for well in wells:
        if (well-1)//8 == column:
            dispSeq.append(well)
    dispSeq[0]=len(dispSeq)-1
    dispSeqStr=""
    for well in dispSeq:
        dispSeqStr = dispSeqStr + str(well) + ";"
    return dispSeqStr[:-1]

def getAspVolStr(aspVol):
    aspVolStr=""
    for vol in aspVol:
        aspVolStr=aspVolStr + str(vol) + ";"
    return aspVolStr[:-1]

def getAspDispMask(aspDispVol):
    """
    Returns an array of 8 integers corresponding to the 8-channel pattern for aspirate or dispense
    :param aspDispVol (array of float)
    :return mask (array of int)
    """
    mask = []
    for vol in aspDispVol:
        if vol == 0 :
            mask.append(0)
        else:
            mask.append(1)
    return mask

def getAspDispMaskStr(mask):
    maskStr = ""
    for i in mask:
        maskStr = maskStr + str(i)
    return maskStr

def getDispVol(volumes,column):
    """
    Returns an array of 8 volumes to dispense in the column of plate j
    :param volumes (array of float) 96 volumes of component i to be dispensed in plate j
    :param column (int) column of plate j
    :return dispVol (array of float) 8 volumes to be dispensed in the column
    """
    dispVol=[0,0,0,0,0,0,0,0]
    for i in range (8):
        dispVol[i] = volumes[column*8+i]
    return dispVol

def getDispVolStr(dispVol):
    dispVolStr = ""
    for vol in dispVol:
        dispVolStr = dispVolStr + str(vol) + ";"
    return dispVolStr[:-1]

def getTipMask(volumes):
    aspTotVol = [0, 0, 0, 0, 0, 0, 0, 0]
    tipMaskStr=""
    for i in range(8):
        for col in range(12):
            aspTotVol[i] = aspTotVol[i] + volumes[col * 8 + i]
        if aspTotVol[i] == 0:
            tipMaskStr=tipMaskStr + "0"
        else:
            tipMaskStr = tipMaskStr + "1"
    return tipMaskStr

def getNumberOfAsp(aspVolVol):

    numberOfAsp=len(aspVolVol)

    return numberOfAsp

if __name__ == "__main__":
    volume=200

    vols=[volume for i in range(96)]

    print("No refill")
    aspDisp=getAspVolDispCol(vols)
    print("Asp = " + str(aspDisp[0]))
    print("Disp = " +  str(aspDisp[1]))
    print("With refill")
    aspDisp = getAspVolDispCol_wRefill(vols)
    print("Asp = " + str(aspDisp[0]))
    print("Disp = " + str(aspDisp[1]))

