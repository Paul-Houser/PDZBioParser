'''
runInParallel
python runInParallel.py -organisms all.txt -positions 1,3,4,5 -numResidues 6 -inputValues P0:ILVF P2:ST -heatmaps -motifID motif1
'''

import os
import time
import argparse
import sys
# from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from GenerateFileList import parseFileNames

# handle command line arguments
def parseArgs():
    parser = argparse.ArgumentParser(
        description='Run C-terminal decameric sequence processing on many files simultaneously')
    parser.add_argument('-organisms', required=True, type=str, 
        help='The text file containing latin names of organisms. Usage: all.txt')
    parser.add_argument('-positions', required=True, type=str, 
        help='The positions to search over, delimited with commas. Usage: 1,3,4,5')
    parser.add_argument('-numResidues', required=True, type=int, 
        help='The number of residues to provide statistics on. Usage: 6')
    parser.add_argument('-inputValues', nargs='+',
        help='The matching positions with desired amino acids. Usage: P0:ILVF P2:ST ... PX:X')
    parser.add_argument('-c', action='store_true', default=False,
        help='Add this flag to create combined CSVs.')
    parser.add_argument('-heatmaps', action='store_true', default=False,
        help='Add this flag to make enrichment heat maps for csv data.')
    parser.add_argument('-motifID', type=str, default="motif",
        help="If heatmaps are created, use this naming convention. Usage: motif1")
    return parser.parse_args()

'''
#RC NOTE: replaced with args.positions.split(',')
# parses input to setup positions array
def parsePositions():
    positions = []
    string = args.positions
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
    return list(set(positions))
'''

#  creates necessary folders to put downloads, csv's, and combined data in.
def makeFolders():
    folders = ["csv", "fastas", "combinedCSVs", "sequenceLists","rawTSV"]
    for folder in folders:
        file_path = str(os.getcwd().replace("\\", "/")) + ("/%s" % folder)
        if not os.path.exists(file_path):
            os.makedirs(file_path)


def distributeWork(positions, fileNames, args):
    callString = ""
    for i in args.inputValues:
        callString += i + " "

    # array of tasks to be completed
    futures = []

    # open thread pool
    with ThreadPoolExecutor(max_workers=8) as executor:
        for x in positions:
            for i in fileNames:
                
                # submit tasks to be completed by threads
                # print(sys.executable + " main.py " + i + " " + str(x) + " " + str(args.numResidues) + " 2 -o -q " + callString)
                futures.append(executor.submit(os.system, (sys.executable + " main.py " + i + " " + str(x) + " " + str(args.numResidues) + " 2 -o -q " + callString)))
        # progress bar
        # for f in tqdm(as_completed(futures), ncols=100, unit="%", total=(len(fileNames) * len(positions))):
        #     pass

"""
createHeatmaps
for each position provided, extract enrichments from the csv files and create heat map pngs for each position.
organisms (list) -- organisms extracted from provided file
motifID (str)    -- identifier for current motif
positions (list) -- positions to create heat maps of
"""
def createHeatmaps(organisms, motifID, positions):
    for p in positions:
        infiles = '/csv/*' + p + '.csv'

        pickle = motifID + '/' + 'position' + p + '.p'
        title = motifID + '_position' + p
        outfile = motifID + '/' + title + '.png'
       
        os.system(sys.executable + " extractCSV.py " + "--files " + infiles + " -outfile " + pickle)
        os.system(sys.executable + " createHeatMap.py " + "--enrichment " + pickle + ' --out ' + outfile + ' -title ' + title + ' -organisms ' + organisms)
        

if __name__ == "__main__":
    args = parseArgs()
    start = time.clock()
    positions = args.positions.split(',')

    makeFolders()

    # exit the program if it can't find the specified file
    if not os.path.isfile(args.organisms):
        print("Could not find file " + args.organisms + " to read.")
        exit(1)

    #  creates file for unfound organisms
    f = open("unfoundOrganisms.txt", "w")
    f.write("Organisms not found on uniprot:\n\n")
    f.close()
    # initialises temp.file so that other programs can know what the input file was , this is a weird solution come back to this
    f = open("~temp.file",'w')
    f.write(args.organisms[:-4]+"_verbose.txt")
    f.close()
    open(args.organisms[:-4]+"_verbose.txt",'w').close()
    distributeWork(positions, parseFileNames(args.organisms), args)
   
    os.remove("~temp.file")
    with open(args.organisms[:-4]+"_verbose.txt",'r') as f:
        uniqueLines = set(f.readlines())
    with open(args.organisms[:-4]+"_verbose.txt",'w') as f:
        for line in sorted(uniqueLines):
            f.write(line)
    # if the user supplies -heatmap flag, create heatmaps for each position provided
    if args.heatmaps:
        print("Creating heat maps...")
        if not os.path.exists(args.motifID):
            os.makedirs(args.motifID)
        createHeatmaps(args.organisms, args.motifID, positions)

    # if the user supplies -c flag, combine CSVs with combineData.py
    if args.c:
        print("Combining CSVs...")
        os.system(sys.executable + " combineData.py " + str(args.organisms) + " " + str(args.positions))

    print('All tasks completed in ' + str(round(time.clock() - start, 2)) + " seconds")
