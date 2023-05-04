def getVolumes(stockConcentration,finalVolume,concentration):
    """
    Returns an array of 96 volumes of component i to be dispensed in plate j
    :param stockConcentration (float) stock concentration of component i
    :param finalVolume (float) final volume of plate j
    :param concentration (array of float) final concentration per well in plate j
    :return volumes (array of float)
    """
    volumes=[]
    for conc in concentration:
        volumes.append(round(conc*finalVolume/stockConcentration,2))
    return volumes

def getWaterVolumes(finalVolume,totVolumes):
    """
    Returns an array of 96 volumes of water to be dispensed in plate j
    :param finalVolume (float) final volume of plate j
    :param totVolumes (array of float) sum of volumes of each component added in plate j
    :return waterVolumes (array of float)
    """
    waterVolumes=[]
    for vol in totVolumes:
        # if it's an empty well
        if vol == 0:
            waterVolumes.append(0)
        else:
            waterVol = finalVolume - vol
            if waterVol > 0:
                waterVolumes.append(finalVolume-vol)
            # if waterVol < 0: don't add water
            else:
                waterVolumes.append(0)
    return waterVolumes

def getWells(volumes):
    """
    Returns an array of active wells
    :param volumes (array of float) 96 volumes of component i to be dispensed in plate j
    :return wells (array of integer)
    """
    wells=[]
    i=1
    for vol in volumes :
        if vol != 0:
            wells.append(i)
        i=i+1
    return wells

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


def getOneTipType(volumes):
    """
    Returns the tip type (1000, 300 or 50 µL)
    :param volumes (array of float) 96 volumes of component i to be dispensed in plate j
    :return tipType (int)
    """
    tipType = "50"
    aspTotVol = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        for col in range(12):
            aspTotVol[i] = aspTotVol[i] + volumes[col * 8 + i]
    i = 0
    if max(aspTotVol) >= 35:
        tipType = "300"
        if max(aspTotVol) >= 275:
            tipType = "1000"
    return tipType

def getTipMask(volumes):
    """
    Returns a string with 8 characters corresponding to 8-channel pattern for tip fetching
    :param volumes (array of float) 96 volumes of component i to be dispensed in plate j
    :return tipMaskStr (str)
    """
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


if __name__ == "__main__":
    volumes=getVolumes(100,940,[1.0, 10.0, 100.0, 0, 0, 0, 0, 0, 100, 0, 0, 1.0, 10.0, 100.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print(volumes)
    aspVolDispCol = getAspVolDispCol(volumes)
    aspVolVol = aspVolDispCol[0]
    dispColCol = aspVolDispCol[1]
    print("aspVolVol =")
    print(aspVolVol)
    print("dispColCol =")
    print(dispColCol)
    wells=getWells(volumes)
    print(wells)
    print(getDispSeqStr(wells,0))
    #aspVol=getAspVol(wells,volumes)
    #aspMask=getAspMask(aspVol)
    #print(aspVol)
    #print(getAspMask(aspVol))
    #print(getDispVolStr(volumes))
    #print(getAspVolStr(aspVol))
    #print(getAspMaskStr(aspMask))
    #print(getDispMask(wells))