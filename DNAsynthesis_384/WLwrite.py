from excelRead import *
from simpleFunctions import *

nucleos_names=['A','C','G','T','M','N','O','P','W','X','Y','Z','U']
nucleos_labware=['Premix' + name for name in nucleos_names ]
nucleos_tipColumn=[1,3,5,7,9,11,1,3,5,7,9,11,12]
nucleos_tipLabware=['Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_1','Tips_1000_2','Tips_1000_2','Tips_1000_2','Tips_1000_2','Tips_1000_2','Tips_1000_2','Tips_1000_1']

filterPlateLabware="FilterPlate"
premixLiquidClass="HighVolume_Premix_DispenseJet_Part"
premixTipsLabware=nucleos_tipLabware[1]
premixVol=50
FlushOutTime=0
incubationTime=0

def writeStep(step,WLFile, nucleo_arrays):
    if (step.pipetType == 0) :
        for i in range(len(nucleos_names)):
            if nucleo_arrays[i+1] != []:
                WLFile.write(nucleotideStepStr(i,nucleo_arrays,step))

    if (step.pipetType == 1) :
         if step.stepName != 0:
                WLFile.write(bufferStepStr(step))


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

def bufferStepStr(step):

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