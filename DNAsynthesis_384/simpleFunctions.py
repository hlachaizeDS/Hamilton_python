def getAspirateVolString(nucleo_array,premixVol):

    aspVol=[0,0,0,0,0,0,0,0]

    for well in nucleo_array:
        aspVol[well%8 -1]=aspVol[well%8 -1]+premixVol

    aspVolStr=""
    for vol in aspVol:
        aspVolStr=aspVolStr + str(vol) + ";"

    return aspVolStr[:-1]

def getTipMaskStr(nucleo_array):

    tipMaskStr=""

    for col in range(1,12+1):
        for row in range(1,8+1):
            if (col-1)*8+row in nucleo_array :
                tipMaskStr = tipMaskStr + "1"
            else :
                tipMaskStr = tipMaskStr + "0"
        tipMaskStr = tipMaskStr + ";"

    return tipMaskStr[:-1]

def getAspirateMaskStr(aspirateVolStr):

    aspVols=aspirateVolStr.split(";")

    aspMaskStr=""
    for vol in aspVols:
        if vol=="0" :
            aspMaskStr=aspMaskStr + "0"
        else:
            aspMaskStr = aspMaskStr + "1"

    return aspMaskStr

def isLastNucleotide(index,nucleo_arrays):

    islast=1
    for i in range(index+1,len(nucleo_arrays)):
        if nucleo_arrays[i]!=[] :
            islast=0
    return islast

