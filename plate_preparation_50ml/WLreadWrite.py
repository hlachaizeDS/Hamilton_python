def getComponentPlateNbr(path):
    """
    Reads component/plate number in a WL
    :param path: (string) path of the WL
    :return nbr: (int) number of the current plate/component (from 0)
    """
    with open(path) as f:
        r = f.readlines()
        nbr = int(r[1])
    return nbr

def writeComponentPlateNbr(path, variable, nbr):
    """
    Writes component/plate number in a WL
    :param path: (string) path of the WL
    :return
    """
    f = open(path, 'w')
    f.write(variable + '\n' + str(nbr))
    f.close()


def writeVariableName(WLfile):
    """
    Writes variable names in the worklist WLfile
    :param WLfile: txt worklist
    :return
    """
    WLfile.write("component" + "\t" + "mode" + "\t" + "labware" + "\t" + "tipType" + "\t" + "tipMask" + "\t" + "volumes" + "\t" + "mask" + "\t" + "dispSeq" + "\n")

def writeVariable(WLfile,componentName, aspDispMode, componentPosition, tipType, tipMask, volStr, maskStr, seq):
    """
    Writes variables in the worklist WLfile
    :param WLfile: txt worklist
    :param componentName: (str)
    :param aspDispMode: (str) boolean 0 = aspirate / 1 = dispense
    :param componentPosition: (str) component position on the deck
    :param tipType: (str) type of tips (50, 300 or 1000)
    :param tipMask: (str) mask to fetch tips (ex: 10100000)
    :param volStr: (str) volume to aspirate or dispense
    :param maskStr: (str) mask to aspirate/dispense (ex: 10100000)
    :param seq: (str) Number of wells and well IDs to dispense
    :return
    """
    WLfile.write(componentName + "\t" + aspDispMode + "\t" + componentPosition + "\t" + tipType + "\t" + tipMask + "\t" + volStr + "\t" + maskStr + "\t" + seq + "\n")
