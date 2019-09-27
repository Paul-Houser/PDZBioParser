from os import listdir
def summaryFile(rawFolder,filteredFolder,outFile):
    writeFile = open(outFile,'w')
    rawLengths = {}
    filteredLengths = {}
    for file in listdir(rawFolder):
        with open(rawFolder+ file, 'r') as readFile:
           rawLengths[file] = len(readFile.readlines()) -1 
    for file in listdir(filteredFolder):
        with open(filteredFolder+ file, 'r') as readFile:
            
            filteredLengths[file] = len(readFile.readlines()) -1
    writeFile.write(",motif Proteins, all proteins\n")
    for organism in filteredLengths:
        writeFile.write(organism+","+str(filteredLengths[organism]) + ","+str(rawLengths[organism]) +"\n")

