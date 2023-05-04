from simpleFunctions import *
from excelRead import *

# extract synthesis format 96 vs 384:
synthesisFormat_96_Boolean = getWellPlateSize(getExcelSheet(path))

nucleos_names=['A','C','G','T','M','N','O','P','W','X','Y','Z','H',"I","J","K","L"]
nucleos_labware=['Premix' + name for name in nucleos_names ]
nucleos_tipColumn=[1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5]
nucleos_tipLabware=['Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_2','Tips_1000_2','Tips_1000_2','Tips_1000_2','Tips_1000_2']

# changed for 384 synth
if synthesisFormat_96_Boolean:
    filterPlateLabware="FilterPlate"
else:
    filterPlateLabware="filter_plate_384"
premixLiquidClass="HighVolume_Premix_DispenseJet_Part"
premixTipsLabware=nucleos_tipLabware[1]
premixVol=50
FlushOutTime=0
incubationTime=0

def writeStep(step,WLFile, nucleo_arrays,usedWells):
    """
    Write step parameters in worklist WLfile
    :param step:  current step parameters
    :param nucleo_arrays (arr) array of 18 arrays containing the wells that should
    receive each nucleotide
    :return
    """
    if step.pipetType == 0: #use 8-channels
        if (step.fromLabware == "nuc_reservoirs") : #use 8-channels to cherry pick nucleotides from reservoirs
            for i in range(len(nucleos_names)):
                if nucleo_arrays[i+1] != []:
                    WLFile.write(nucleotideStepStr(i,nucleo_arrays,step))
        else: #use 8-channels to dispense in "used wells"
            WLFile.write(channel8StepStr(usedWells, step))

    else: #use 96-head
        WLFile.write(head96StepStr(step))


def nucleotideStepStr(index,nucleo_arrays,step):

    #StepName
    stepStr='Add ' + nucleos_names[index]

    #pipetType
    stepStr= stepStr + "\t" + str(step.pipetType)

    #Incubation time
    isLast=isLastNucleotide(index+1,nucleo_arrays)
    if isLast:
        stepStr = stepStr + "\t" + str(step.incubationTime)
    else:
        stepStr = stepStr + "\t" + str(incubationTime)

    # FlushOut time
    isLast=isLastNucleotide(index+1,nucleo_arrays)
    if isLast:
        stepStr = stepStr + "\t" + str(step.FlushOutTime)
    else:
        stepStr = stepStr + "\t" + str(FlushOutTime)

    # repeats
    stepStr = stepStr + "\t" + str(step.repeats)

    #From labware
    stepStr = stepStr + "\t" + nucleos_labware[index]

    #To labware
    stepStr = stepStr + "\t" + filterPlateLabware

    #Liquid Class
    stepStr = stepStr + "\t" + premixLiquidClass

    #PremixTipsLabware
    stepStr = stepStr + "\t" + nucleos_tipLabware[index]

    #Tip Column
    stepStr = stepStr + "\t" + str(nucleos_tipColumn[index])

    #Aspirate Volume
    premixVol = step.Volume
    stepStr = stepStr + "\t" + getAspirateVolString(nucleo_arrays[index+1],premixVol)

    #Aspirate Mask
    stepStr = stepStr + "\t" + getAspirateMaskStr(getAspirateVolString(nucleo_arrays[index+1], premixVol))

    #DispVol
    stepStr = stepStr + "\t" + str(step.Volume)

    # TipMask
    stepStr = stepStr + "\t" + getTipMaskStr(nucleo_arrays[index+1])

    #End of line
    stepStr = stepStr + "\n"
    return stepStr

def channel8StepStr(usedWells,step):
    # StepName
    stepStr = step.stepName

    # pipetType
    stepStr = stepStr + "\t" + str(step.pipetType)

    # Incubation time
    stepStr = stepStr + "\t" + str(step.incubationTime)

    # FlushOut time
    stepStr = stepStr + "\t" + str(step.FlushOutTime)

    # repeats
    stepStr = stepStr + "\t" + str(step.repeats)

    # From labware
    stepStr = stepStr + "\t" + step.fromLabware

    # To labware
    stepStr = stepStr + "\t" + filterPlateLabware

    # Liquid Class
    stepStr = stepStr + "\t" + premixLiquidClass

    #  Tip Labware
    stepStr = stepStr + "\t" + step.TipLabware

    # Tip Column
    stepStr = stepStr + "\t" + "6"

    #Aspirate Volume
    print("usedWells =")
    print(usedWells)
    stepStr = stepStr + "\t" + getAspirateVolString(usedWells,step.Volume)

    #Aspirate Mask
    stepStr = stepStr + "\t" + getAspirateMaskStr(getAspirateVolString(usedWells,step.Volume))

    #DispVol
    stepStr = stepStr + "\t" + str(step.Volume)

    # TipMask
    stepStr = stepStr + "\t" + getTipMaskStr(usedWells)

    #End of line
    stepStr = stepStr + "\n"
    return stepStr

def head96StepStr(step):

        # StepName
        stepStr = step.stepName

        # pipetType
        stepStr = stepStr + "\t" + str(step.pipetType)

        # Incubation time
        stepStr = stepStr + "\t" + str(step.incubationTime)

        # FlushOut time
        stepStr = stepStr + "\t" + str(step.FlushOutTime)

        # repeats
        stepStr = stepStr + "\t" + str(step.repeats)

        # From labware
        stepStr = stepStr + "\t" + step.fromLabware

        # To labware
        stepStr = stepStr + "\t" + filterPlateLabware

        # Liquid Class
        stepStr = stepStr + "\t" + step.LiquidClass

        #  Tip Labware
        stepStr = stepStr + "\t" + step.TipLabware

        # Tip Column
        stepStr = stepStr + "\t" + "0"

        # Aspirate Volume
        stepStr = stepStr + "\t" + str(step.Volume)

        # Aspirate Mask
        stepStr = stepStr + "\t" + "0"

        # DispVol
        stepStr = stepStr + "\t" + str(step.Volume)

        # TipMask
        stepStr = stepStr + "\t" + "0"

        # End of line
        stepStr = stepStr + "\n"
        return stepStr