#!/usr/bin/python3

import csv
from itertools import repeat

folder = "expASel"
expPlanFileName = "MyData.csv"

generations = 30
replicate = 10
foldertime = 0
initSize = 100
nbPop = 100
nbPopHalf = int(nbPop/2)
nbAllele = 2
# iniAllFreqEq = 0.5
fecundity = 2

launcherFileName = "launcher"


launcherFileCrop = "Universe=vanilla\nExecutable=/usr/bin/python3\nshould_transfer_files=no\ninput=/dev/null\noutput=condor.out\nerror=condor.error\nlog=condor.log\nrequirements=( HAS_ASREML =?= False )\nrequest_memory=4G\ngetenv=true\n"

launcherFileR = "Universe=vanilla\nExecutable=/usr/bin/python3\nshould_transfer_files=no\ninput=/dev/null\noutput=condor.out\nerror=condor.error\nlog=condor.log\nrequirements=( HAS_ASREML =?= False )\nrequest_memory=1G\ngetenv=true\n"

all1s = '{' + ','.join(str(e) for e in list(repeat(1, nbPop))) + '}'
tempHalf = list(repeat(0, nbPopHalf)) + list(repeat(1, nbPopHalf))
half1 = '{' + ','.join(str(e) for e in tempHalf) + '}'
continuous = '{' + ','.join(str(int(e/nbPop)) for e in list(range(0, nbPop))) + '}'

paramNames = ["folder:", "generations:", "replicates:", "folder_time:",\
        "init_size:", "nb_pop:", "nb_allele:",\
        "fecundity:", "carr_capacity:",\
        "percentSelf:", "mut_rate:", "nb_marker:", "fitness_equal:", "optimum:"]

paramMatrix = [[10, 100, 1000], [0, 0.5, 0.95], [0.001, 0.01, 0.1],\
        ["fit1.csv", "fit5.csv", "fit10.csv"],\
        [all1s, half1, continuous]]

with open(expPlanFileName) as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for row in reader:
        parameters = [folder+ '_'.join(row), generations, replicate, foldertime, initSize,\
                nbPop, nbAllele, fecundity]
        for paramNb, indices in enumerate(row):
            if paramNb == 3 and indices == '1':
                nbMarker = 10
                parameters.append(nbMarker)
                parameters.append(paramMatrix[paramNb][int(indices)-1])
            elif paramNb == 3 and indices == '2':
                nbMarker = 11
                parameters.append(nbMarker)
                parameters.append(paramMatrix[paramNb][int(indices)-1])
            elif paramNb == 3 and indices == '3':
                nbMarker = 20
                parameters.append(nbMarker)
                parameters.append(paramMatrix[paramNb][int(indices)-1])
            else:
                parameters.append(paramMatrix[paramNb][int(indices)-1])

        stringToFile = ""
        for paramIndex, paramValue in enumerate(parameters):
            if paramIndex == 12 and parameters[paramIndex] == "0":
                stringToFile += "#" + paramNames[paramIndex] + str(parameters[paramIndex]) + "\n"
            else:
                stringToFile = stringToFile + paramNames[paramIndex] + str(parameters[paramIndex]) + "\n"

        stringToFile += "#outputs:{genotype}"
        fileNameToWrite = folder + "_" + '_'.join(row) + ".set"

        fileToWrite = open(fileNameToWrite, "w")
        fileToWrite.write(stringToFile)
        fileToWrite.close()

        launcherFileCrop = launcherFileCrop + "\nArguments = /home/deap/aknainojika/cropmetapop/CropMetaPop.py /home/deap/aknainojika/" + fileNameToWrite + "\nqueue\n\n"
        launcherFileR = launcherFileR + "\nArguments = /home/deap/aknainojika/analysisSel.py /home/deap/aknainojika/" + folder + '_'.join(row) + " " + str(replicate) + " " + str(nbPop) + " " + str(nbMarker) + " " + str(nbAllele) + "\nqueue\n\n"
launchFileCrop = open(launcherFileName + "Sel", "w")
launchFileCrop.write(launcherFileCrop)
launchFileCrop.close()

launchFileR = open(launcherFileName+"SelPy", "w")
launchFileR.write(launcherFileR)
launchFileR.close()
