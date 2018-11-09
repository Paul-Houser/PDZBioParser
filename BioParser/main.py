#  import dependencies
import argparse
import datetime
import time
import os
from dl import getFasta
from structure import structure
from parse import read_file
from fileOutput import *

# [0, False] is the default sort, that runInParallel uses
howToSort = [0, False]

#  setup variables
currentFile = ""
searchPosition = None
fileNames = ""
numResidues = None

#  unfound organisms
unFound = ""

#  create dict of all the specified positions and criteria
importantPositions = []

#  creates a list of all numerical important positions
pList = []


def parseArgs():

    #  handle command line arguments
    parser = argparse.ArgumentParser(
        description='Process C-terminal decameric matchingSequences')

    parser.add_argument('file', metavar='file', type=str,
                        nargs=1, help='The file to be parsed')
    parser.add_argument('position', metavar='position', type=int,
                        nargs=1, help='The position to search in')
    parser.add_argument('numResidues', metavar='numResidues', type=int,
                        nargs=1, help='The number of residues to provide statistics on.')
    parser.add_argument('sort', metavar='sort', type=int,
                        nargs=1, help='How to sort final output')
    parser.add_argument('-o', action='store_true',
                        help='Add this flag to enable file output.')
    parser.add_argument('-q', action='store_true',
                        help='Add this flag to silence printout of ratios')
    parser.add_argument('inputValues', nargs='+',
                        help='The matching positions with desired amino acids. Usage: P0:ILVF P2:ST ... PX:X')

    return parser.parse_args()


def makeFile():
    path = str(os.getcwd()) + "/unfoundOrganisms.txt"
    if not os.path.exists(path):
        f = open(path, "w")
        f.close()


# assigning howToSort from command line input
# first value is 0,1 meaning key or value, second is reverse = true or false
def assignSort(sort):
    global howToSort

    if sort == 0:
        howToSort = [1, False]
    if sort == 1:
        howToSort = [1, True]
    if sort == 2:
        howToSort = [0, False]
    if sort == 3:
        howToSort = [0, True]

#  creates necessary folders to put downloads, csv's, and combined data in.
def makeFolders():
    folders = ["csv", "fastas", "combinedCSVs", "sequenceLists"]
    for folder in folders:
        file_path = str(os.getcwd().replace("\\", "/")) + ("/%s" % folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)





#  gets all important positions from args.inputValues and adds them to the list 'importantPositions'
def getImportantPositions(inputValues):
    for i in inputValues:
        currentValue = []
        currentPosition = ""

        for j in range(1, len(i)):
            if i[j].isdigit():
                currentPosition += i[j]
            elif i[j] == ":":
                currentValue.append(int(currentPosition))
            else:
                currentValue.append(i[j])
        importantPositions.append(currentValue)

def getPosList():
    for i in importantPositions:
        pList.append(i[0])

def setUpStructure(silent, o):
    for file in fileNames:

        # setup class
        currentStructure = structure()
        currentStructure.organism = file
        currentStructure.numResidues = numResidues
        currentStructure.searchPosition = searchPosition
        currentStructure.pList = pList
        currentStructure.importantPositions = importantPositions
        currentStructure.howToSort = howToSort

        # parse file
        currentStructure = read_file(currentStructure)
        if not (currentStructure):
            unFoundOrgs(file.split(".")[0])
            continue

        # file writing
        setupOutputFile(currentStructure)
        printData("csv/" + file.split(".")[0] + ".csv", "Frequencies of all amino acids in file:",
                currentStructure.freqAll, True, searchPosition, False, silent)
        printData("csv/" + file.split(".")[0] + ".csv", "Frequencies of all amino acids in the last " + str(
            currentStructure.numResidues) + " positions (non-redundant):", currentStructure.freqLastN, True, searchPosition, False, silent)
        printData("csv/" + file.split(".")[0] + ".csv", "Frequencies of all amino acids at the given position (non-redundant)",
                currentStructure.freqPositional, True, searchPosition, False, silent)
        printData("csv/" + file.split(".")[0] + ".csv", "Enrichment ratios for each amino acid at given position",
                currentStructure.enrichment, False, searchPosition, howToSort, silent)
        if (o):
            printSequencesAndIdentifiers(currentStructure)





#####################################################################################

def main():
    global currentFile
    global searchPosition
    global fileNames
    global numResidues

    args = parseArgs()

    #  setup variables
    currentFile = ""
    searchPosition = args.position[0]
    fileNames = args.file[0].split(",")
    numResidues = args.numResidues[0]

    #  start timer
    startTime = time.clock()

    

    #  controls print out to console
    silent = args.q

    makeFile()

    assignSort(args.sort[0])

    makeFolders()

    getImportantPositions(args.inputValues)

    getPosList()

    setUpStructure(silent, args.o)

    unFoundOrgs(unFound)

    if not silent:
        print("Parser completed in", round(time.clock() - startTime, 2), "seconds")

        

main()
