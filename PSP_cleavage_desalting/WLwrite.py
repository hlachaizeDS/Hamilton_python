def writeDSparameters(WL_DSparameters, DSparameters):
    WL_DSparameters.write(str(DSparameters.shakingTime) + "\t" + str(DSparameters.transferVol1) + "\t" + str(DSparameters.transferVol2) + "\t" + str(DSparameters.cleavageTime) + "\t" + str(DSparameters.bioshakeCleavageStir) + "\t" + str(DSparameters.bioshakeCleavageTemp) + "\t" + str(DSparameters.isopropIncubTime) + "\t" + str((DSparameters.isopropMixTransferVol)/2+20) + "\t" + str(DSparameters.desaltingVacuumTime)+ "\t" + str(DSparameters.ethanolDryingTime))

def writeVariableName(WLfile):
    """
    Writes variable names in the worklist WLfile
    :param WLfile: txt worklist
    :return
    """
    WLfile.write("reagent" + "\t" + "mode" + "\t" + "labware" + "\t" + "liquidClass" + "\t" + "tip" + "\t" + "tipMask" + "\t" + "volumes" + "\t" + "mask" + "\t" + "dispSeq" + "\t" + "numberOfAsp"  + "\n")

def writeVariable(WLfile, i, pipettingParameters, aspDispMode, labware, tipColumn, tipMask, volStr, maskStr, seq, numberOfAsp):
    """
    Writes variables in the worklist WLfile
    :param WLfile: txt worklist
    :param i: (int) step number
    :param pipettingParameters: (arr) array of reagents, liquid classes, volumes and destinations plates
    :param aspDispMode: (str) boolean 0 = aspirate / 1 = dispense
    :param labware: (str) labware to aspirate or dispense
    :param tipColumn: (int) column 1, 2 or 3 of "Tips_1000_PSP" tip box
    :param tipMask: (str) mask to fetch tips (ex: 10100000)
    :param volStr: (str) volume to aspirate or dispense
    :param maskStr: (str) mask to aspirate/dispense (ex: 10100000)
    :param seq: (str) Number of wells and well IDs to dispense
    :param numberOfAsp: (int) number of aspiration per step
    :return
    """
    WLfile.write(pipettingParameters[0][i] + "\t" + aspDispMode + "\t" + labware + "\t" + pipettingParameters[1][i] + "\t" + str(tipColumn) + "\t" + tipMask + "\t" + volStr + "\t" + maskStr + "\t" + seq + "\t" + str(numberOfAsp) + "\n")
