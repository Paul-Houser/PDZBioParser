import os
import datetime

#  Sets up the output CSV's


def setupOutputFile(structure):
    now = datetime.datetime.now()
    fileName = "csv/" + structure.organism.split(".")[0] + ".csv"
    # clears contents of outputFile
    open(fileName.split(".")[0] +
         str(structure.searchPosition) + ".csv", 'w').close()

    # adds headers for .csv
    f = open(fileName.split(".")[0] +
             str(structure.searchPosition) + ".csv", 'a')
    f.write("File name: " + fileName.split("csv/")[1] + ",,\n")
    lineToWrite = "Requirements: "
    for item in structure.importantPositions:
        lineToWrite += "P" + str(item[0]) + ":" + ''.join(str(item[x])
                                                          for x in range(1, len(item))) + " "
    lineToWrite += ",,"
    f.write(lineToWrite + "\n")
    f.write("Comparison Position: " + str(structure.searchPosition) + ",,\n")
    f.write("Timestamp: " + str(now.month) + "/" + str(now.day) + "/" +
            str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ",,\n")
    f.write("\nAmino Acid,# Occurrences,Percentage\n")
    f.close()

# create csv of sequences with identifiers


def printSequencesAndIdentifiers(structure):
    writeFile = "sequenceLists/" + structure.organism.split(".")[0]
    f = open(writeFile.split(".")[0] + ".tsv", 'w')
    f.write("Sequence:\tIdentifier:\n")
    for i in range(0, len(structure.sequences)):
        f.write(structure.sequences[i] + "\t" + structure.sequenceLabels[i])
    f.close()

#  print data from one dictionary into console and file


def printData(fileName, header, dict, percents, searchPosition, howToSort, silent):
    f = open(fileName.split(".")[0] + str(searchPosition) + ".csv", 'a')
    if not silent:
        print(header)
    f.write("\n" + header + ",,\n")
    totalChars = sum(dict.values())
    if not howToSort:
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    else:
        dict = sorted(
            dict.items(), key=lambda x: x[howToSort[0]], reverse=howToSort[1])
    for a in dict:
        if totalChars > 0:  # and a[1] > 0:
            percentString = ""
            if percents:
                percentString = str(round(a[1] / totalChars * 100, 4)) + "%"
            if not silent:
                print(a[0], a[1], percentString)
            f.write(a[0] + "," + str(a[1]) + "," + percentString + "\n")
    f.close()

#  creates a file for organism proteoms that couldnt be found on uniprot
def unFoundOrgs(unFound):
    f = open("unfoundOrganisms.txt", "r")
    lines = f.readlines()
    for line in lines:
        if line.replace("\n", "") == unFound:
            unFound = ""
    f.close()

    f = open("unfoundOrganisms.txt", "a")
    if unFound != "":
        f.write(unFound + "\n")
    f.close()
