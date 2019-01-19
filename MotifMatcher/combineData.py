# Raiden van Bronkhorst, Milo Rupp, Sergey Datskiy
# November, 2017, December 2018

import os, argparse
from GenerateFileList import parseFileNames


# checks if file exists
def fileExists(readFile):
    return os.path.isfile(readFile)

# def parsePositions
def parsePositions(posString):
    positions = []
    stream = ""
    for i in range(0, len(posString)):
        if posString[i].isdigit():
            stream += posString[i]
        elif posString[i] == ",":
            positions.append(int(stream))
            stream = ""
    if (posString[-1].isdigit()):
        positions.append(int(posString[-1]))
    positions = list(set(positions))
    return positions


# main function
if __name__ == "__main__":

    #what is this in the next line?
    # from tqdm import tqdm
    fileNames = []

    parser = argparse.ArgumentParser(description='Combine created CSVs into single CSVs for each position')
    parser.add_argument('file', metavar='file', type=str, nargs=1, help='The text file containing names of organisms')
    parser.add_argument('positions', metavar='positions', type=str, nargs=1, help='The positions to search in')
    args = parser.parse_args()
    positions = []
    folderPos = os.getcwd()
    fileNames = parseFileNames(args.file[0])

    #run fileExists
  
    if True:

        positions = parsePositions(args.positions[0])

        

        for p in positions:
            combinedFile = open(folderPos+"/combinedCSVs/combined" + str(p) + ".csv", "w")

            for index in range(115):

                for fileName in fileNames:
                    fileName = folderPos + '/csv/'+fileName.split(".")[0] + str(p) + ".csv"

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
