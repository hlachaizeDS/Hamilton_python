def getAspirateVolString(nucleo_array,premixVol):
    """
    Returns a string with volumes of premix to be aspirated with 8-channels
    :param nucleo_array (arr of int) array containing the wells that should
    receive one of the  nucleotides
    :param premixVol (flt) volume of premix to be dispensed with 8-channels
    :return aspVolStr (str) 8 volumes of premix to aspirate
    """
    aspVol=[0,0,0,0,0,0,0,0]

    for well in nucleo_array:
        aspVol[well%8 -1]=aspVol[well%8 -1]+premixVol
    aspVolStr = ""

    for vol in aspVol:
        if vol != 0:
            vol = vol + 10 #add 10 µL of conditionning volume
        aspVolStr = aspVolStr + str(vol) + ";"
    return aspVolStr[:-1]

def getTipMaskStr(nucleo_array):
    """
    Returns a string with 8-channel patterns for nucleotide dispense
    :param nucleo_array (arr of int) array containing the wells that should
    receive one of the  nucleotides
    :return tipMaskStr (str)
    """
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
    """
    Returns a string with 8-channel pattern for aspirate
    :param aspirateVolStr (str) 8 volumes of premix to aspirate
    :return aspMaskStr (str)
    """
    aspVols=aspirateVolStr.split(";")

    aspMaskStr=""
    for vol in aspVols:
        if vol=="0" :
            aspMaskStr=aspMaskStr + "0"
        else:
            aspMaskStr = aspMaskStr + "1"

    return aspMaskStr

def isLastNucleotide(index,nucleo_arrays):
    """
    Returns a boolean indicating if it's the last nucleotide type to be dispensed
    :param index (int) corresponds to the current nucleotide type
    :param nucleo_arrays (arr) array of 18 arrays containing the wells that should
    receive each nucleotide
    :return isLast (int)
    """
    islast=1
    for i in range(index+1,len(nucleo_arrays)):
        if nucleo_arrays[i]!=[] :
            islast=0
    return islast

