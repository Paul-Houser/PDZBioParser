# Paul Houser, Milo Rupp, Raiden van Bronkhorst, Jordan Valgardson

# September, 2017

# This program sets up variables and the structure object specific to the protein being parsed, and
# then calls parse.py on the current organism.

#  import dependencies
import argparse
import datetime
import time
import os
import math
from structure import structure
from parse import read_file
from fileOutput import *

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
    parser.add_argument('motifs', nargs='+',
                        help='The matching positions with desired amino acids. Usage: P0:ILVF P2:ST ... PX:X')
    return parser.parse_args()


#  gets all important positions from args.motifs and adds them to the list 'importantPositions'
def getImportantPositions(motifs):
    importantPositions = []
    for i in motifs:
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
    return importantPositions

# sets up object containing all output information
def setUpStructure(fileNames, numResidues, searchPosition, pList, importantPositions, howToSort, silent, o):
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
        # if file cannot be found, add to unfound organisms
        
        currentStructure = read_file(currentStructure)
        if not (currentStructure):
            unFoundOrgs(file.split(".")[0])
            continue
       
        file = currentStructure.organism

        a = time.time()
        # file writing
        setupOutputFile(currentStructure)
        printData("csv/" + file.split(".")[0] + ".csv", "Frequencies of all amino acids at search position:",
                currentStructure.freqMotifPositional, True, searchPosition, False, silent)
        printData("csv/" + file.split(".")[0] + ".csv", "Frequencies of all amino acids in the last " + str(
            currentStructure.numResidues) + " positions (non-redundant):", currentStructure.freqNonRedMotifPositional , True, searchPosition, False, silent)
        
        printData("csv/" + file.split(".")[0] + ".csv", "Frequencies of all amino acids at the given position (non-redundant)",
                currentStructure.freqAllPositional, True, searchPosition, False, silent)
        printData("csv/" + file.split(".")[0] + ".csv", "Enrichment ratios for each amino acid at given position",
                currentStructure.enrichment, False, searchPosition, howToSort, silent)
        if (o):
            printSequencesAndIdentifiers(currentStructure)
        
        
if __name__ == "__main__":
    args = parseArgs()

    # creates the file to hold unfound organisms
    path = str(os.getcwd()) + "/unfoundOrganisms.txt"
    if not os.path.exists(path):
        open(path, "w").close()

    # initializes howToSort based on command line input
    # first value is 0,1 meaning key or value, second is reverse = true or false
    # [0, False] is the default sort
    howToSort = [0, False]
    sort = args.sort[0]
    if sort == 0:
        howToSort = [1, False]
    if sort == 1:
        howToSort = [1, True]
    if sort == 2:
        howToSort = [0, False]
    if sort == 3:
        howToSort = [0, True]

    importantPositions = getImportantPositions(args.motifs)
    pList = []
    for i in importantPositions:
        pList.append(i[0])

    # start timer
    startTime = time.clock()

    setUpStructure(args.file[0].split(","), args.numResidues[0], args.position[0], pList, importantPositions, howToSort, args.q, args.o)

    if not args.q:
        print("Parser completed in", round(time.clock() - startTime, 2), "seconds")
