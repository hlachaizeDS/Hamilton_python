from excelRead import *

positionID=[]

def writeColumnName(WLFile):
    WLFile.write("positionID" + "\t" + "loopNbr" + "\t" + "lastTipMask" + "\n" + "\t" + str(getLoopNbr()) + "\t" + getLastTipMask() + "\n")

def writeValue(WLFile,i):
        WLFile.write(str(i) + "\n")

def positionIDstr(i):
    positionIDstr = str(usedWells[i])
    return positionIDstr

#def tipMask(col):
 #   tipMask = str(usedWells[col])
  #  return tipMask

print(positionIDstr(0))





