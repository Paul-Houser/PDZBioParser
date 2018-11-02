#  import dependencies
import argparse
import datetime
import time
import os
from dl import getFasta
from structure import structure
from parse import read_file
from fileOutput import *

#  start timer
startTime = time.clock()

#  unfound organisms
unFound = ""

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

args = parser.parse_args()

#  setup global variables
currentFile = ""
searchPosition = args.position[0]
fileNames = args.file[0].split(",")
numResidues = args.numResidues[0]

path = str(os.getcwd()) + "/unfoundOrganisms.txt"
if not os.path.exists(path):
    f = open(path, "w")
    f.close()

# assigning howToSort from command line input
# first value is 0,1 meaning key or value, second is reverse = true or false
if args.sort[0] == 0:
    howToSort = [1, False]
if args.sort[0] == 1:
    howToSort = [1, True]
if args.sort[0] == 2:
    howToSort = [0, False]
if args.sort[0] == 3:
    howToSort = [0, True]

#  creates necessary folders to put downloads, csv's, and combined data in.
folders = ["csv", "fastas", "combinedCSVs", "sequenceLists"]
for folder in folders:
    file_path = str(os.getcwd().replace("\\", "/")) + ("/%s" % folder)
    if not os.path.exists(file_path):
        os.makedirs(file_path)

#  controls print out to console
silent = args.q

#  create dict of all the specified positions and criteria
importantPositions = []

#  gets all important positions from arts.inputValues and adds them to the list 'importantPositions'
for i in args.inputValues:
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

#  creates a list of all numerical important positions
pList = []
for i in importantPositions:
    pList.append(i[0])

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

    # console printing
    # print(currentStructure.organism.split(".")[0])
    # print(currentStructure.sequences[0])
    # print(currentStructure.sequenceLabels[0])

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
    if (args.o):
        printSequencesAndIdentifiers(currentStructure)


unFoundOrgs(unFound)

if not silent:
    print("Parser completed in", round(time.clock() - startTime, 2), "seconds")
