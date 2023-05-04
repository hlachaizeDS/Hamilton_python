def writeVariableName(WL_synthesis_PSP_parameters):
    WL_synthesis_PSP_parameters.write("performSynthesis" + "\t" + "performPSPwashes" + "\t" + "performCleavageDesalting" + "\t" + "year" + "\t" + "month" + "\t" + "day" + "\t" + "hour" + "\t" + "minute" + "\n")

def writeRunParameters(WL_synthesis_PSP_parameters, runParameters, PSPdate):
    for parameter in runParameters:
        WL_synthesis_PSP_parameters.write(str(parameter) + "\t")
    for i in range (4):
        WL_synthesis_PSP_parameters.write(str(PSPdate[i]) + "\t")
    WL_synthesis_PSP_parameters.write(str(PSPdate[4]))
    return