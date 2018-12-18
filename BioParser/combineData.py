import os, argparse
from GenerateFileList import parseFileNames
# from tqdm import tqdm
fileNames = []

parser = argparse.ArgumentParser(description='Combine created CSVs into single CSVs for each position')
parser.add_argument('file', metavar='file', type=str, nargs=1, help='The text file containing names of organisms')
parser.add_argument('positions', metavar='positions', type=str, nargs=1, help='The positions to search in')
args = parser.parse_args()
positions = []
readFile = args.file[0]

# checks if file exists
if not os.path.isfile(readFile):
    print("Could not find file " + readFile + " to read.")
    exit(1)

def parsePositions():
    global positions

    string = args.positions[0];
    stream = ""
    for i in range(0, len(string)):
        if string[i].isdigit():
            stream += string[i]
        elif string[i] == ",":
            positions.append(int(stream))
            stream = ""
    if (string[-1].isdigit()):
        positions.append(int(string[-1]))
    positions = list(set(positions))


parsePositions()
fileNames = parseFileNames(readFile)
print(fileNames)
for p in positions:
    combinedFile = open("combinedCSVs/combined" + str(p) + ".csv", "w")

    for index in range(0,115):

        for fileName in fileNames:
            fileName = 'csv/'+fileName.split(".")[0] + str(p) + ".csv"
            
            if os.path.isfile(fileName):
                file = open(fileName, "r")
                lines = file.readlines()
                if index < len(lines):
                    line = lines[index]

                    combinedFile.write(line.split("\n")[0])
                    if len(line.strip("\n")) > 0:
                        combinedFile.write(",,")
                    else:
                        combinedFile.write(",,,,")
                else:
                    combinedFile.write(",,,,")
                file.close()
        combinedFile.write("\n")
    combinedFile.close()
