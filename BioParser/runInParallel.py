
import os
import time
import argparse
import sys
# from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# handle command line arguments
parser = argparse.ArgumentParser(
    description='Run C-terminal decameric sequences on many files simultaneously')

parser.add_argument('file', metavar='file', type=str, nargs=1,
                    help='The text file containing latin names of organisms')
parser.add_argument('positions', metavar='positions', type=str,
                    nargs=1, help='The positions to search in')
parser.add_argument('numResidues', metavar='numResidues', type=int,
                    nargs=1, help='The number of residues to provide statistics on.')
parser.add_argument('inputValues', nargs='+',
                    help='The matching positions with desired amino acids. Usage: P0:ILVF P2:ST ... PX:X')
parser.add_argument('-c', action='store_true',
                    help='Add this flag to create combined CSVs.')

args = parser.parse_args()

#  initializing necessary vaiables to run multiple threads of parse.py
fileName = args.file[0]
start = time.clock()
fileNames = []
futures = []
tasks = 0
completed = 0
positions = []
callString = ""

# exit the program if it can't find the specified file
if not os.path.isfile(fileName):
    print("Could not find file " + fileName + " to read.")
    exit(1)

#  creates file for unfound organisms
f = open("unfoundOrganisms.txt", "w")
f.write("Organisms not found on uniprot:\n\n")
f.close()

# parses input to setup positions array
def parsePositions():
    global positions
    global callString

    string = args.positions[0]
    stream = ""

    # for each character in the input, if it's a digit, concatenate to number
    # otherwise the number is done being read, add to positions
    for i in range(0, len(string)):
        if string[i].isdigit():
            stream += string[i]
        elif string[i] == ",":
            positions.append(int(stream))
            stream = ""
    # add the last digit to the array, eliminates need for comma 1,2,3,4,5,6>,<
    if (string[-1].isdigit()):
        positions.append(int(string[-1]))
    positions = list(set(positions))

    for i in args.inputValues:
        callString += i + " "

# parses input to setup files to call parse.py with
def parseFileNames():
    global fileName
    with open(fileName, "r") as file:
        lines = file.readlines()
        for line in lines:
            fileName = line.replace(" ", "_")
            fileName = fileName.strip("\n") + ".fasta"
            fileNames.append(fileName)


parsePositions()
parseFileNames()

total = len(fileNames) * len(positions)

# open thread pool
with ThreadPoolExecutor(max_workers=8) as executor:
    for x in positions:
        for i in fileNames:
            # add tasks to complete to the "future" list
            # print(" main.py " + i + " " + str(x) + " " + str(args.numResidues[0]) + "2 -o " + callString)
            futures.append(executor.submit(os.system, (sys.executable + " main.py " + i +
                                                       " " + str(x) + " " + str(args.numResidues[0]) + " 2 -o -q " + callString)))
    # show progress bar
    # for f in tqdm(as_completed(futures), ncols=100, unit="%", total=(len(fileNames) * len(positions))):
        # pass

if args.c:  # if the user supplies -c flag, combine CSVs with combineData.py
    print("Combining CSVs...")
    os.system(sys.executable + " combineData.py " +
              str(args.file[0]) + " " + str(args.positions[0]))
print('All tasks completed in ' + str(round(time.clock() - start, 2)) + " seconds")
