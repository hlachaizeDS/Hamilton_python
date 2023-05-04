filterPlateLabware="FilterPlate"

def writeVariableName(WLfile):
    """
    Writes variable names in the worklist WLfile
    :param WLfile: txt worklist
    :return
    """
    WLfile.write("step" + "\t" + "mode" + "\t" + "labware" + "\t" + "liquidClass" + "\t" + "tip" + "\t" + "tipMask" + "\t" + "volumes" + "\t" + "mask" + "\t" + "dispSeq" + "\t" + "numberOfAsp" + "\t" + "incubationTime" + "\t" + "flushOutTime" + "\t" + "repeat" + "\n")

def writeVariable(WLfile,step, aspDispMode, labware, tipColumn, tipMask, volStr, maskStr, seq, numberOfAsp):
    """
    Writes variables in the worklist WLfile
    :param WLfile: txt worklist
    :param step (class)
    :param aspDispMode: (str) boolean 0 = aspirate / 1 = dispense
    :param tipColumn: (int) column 1, 2 or 3 of "Tips_1000_PSP" tip box
    :param tipMask: (str) mask to fetch tips (ex: 10100000)
    :param volStr: (str) volume to aspirate or dispense
    :param maskStr: (str) mask to aspirate/dispense (ex: 10100000)
    :param seq: (str) Number of wells and well IDs to dispense
    :param numberOfAsp: (int) number of aspiration per step
    :return
    """
    WLfile.write(step.stepName + "\t" + aspDispMode + "\t" + labware + "\t" + step.liquidClass + "\t" + str(tipColumn) + "\t" + tipMask + "\t" + volStr + "\t" + maskStr + "\t" + seq + "\t" + str(numberOfAsp) + "\t" + str(step.incubationTime) + "\t" + str(step.flushOutTime) + "\t" + str(step.repeats) + "\n")

