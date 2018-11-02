#  bioParser
#  Milo Rupp, Raiden van Bronkhorst, Paul Houser
#  10/12/17

#  import dependencies
import argparse, datetime, time, os
from dl import getFasta
from structure import structure

#  interpret fasta file
def read_file(currentStructure):

    matchingSequences = [] #  matchingSequences holds the last numResidues residues that match the given criteria
    sequences = [] # sequences holds the last numResidues residues of each sequence

    # make sure the fasta is downloaded
    if not getFasta(currentStructure.organism,True):
        return False
    
    noPathFileName = currentStructure.organism
    fileName = "fastas/" + noPathFileName

    #  opens fasta file to be parsed
    with open(fileName, "r") as file:

        lines = file.readlines()
        lines.append(">")

        currentSequence = "" #  The current chunk of amino acids
        sequenceLabel = ""
        currentLabel = ""

        for line in lines:

            #  A '>' signifies the start of a new protein in the fasta files.
            if line[0] == ">":
                
                sequenceLabel = currentLabel
                currentLabel = line

                if currentSequence != "":

                    for char in currentSequence:
                        currentStructure.freqAll[char] += 1
                    
                    currentSequence = currentSequence[-currentStructure.numResidues:] # sets currentSequence to the last numResidues of itself
                    sequences.append(currentSequence)

                    #  Only appends the current sequence to the list of matching sequences IF all important positions match
                    shouldAppend = True
                    for i in range(0, len(currentStructure.pList)):
                        if not currentSequence[len(currentSequence) - currentStructure.pList[i] - 1] in currentStructure.importantPositions[i]:
                            shouldAppend = False
                            break

                    #  sequence is appended if it matches criteria
                    if shouldAppend:
                        matchingSequences.append(currentSequence)
                        currentStructure.sequenceLabels.append(sequenceLabel)

                    #  resets currentSequence so the next sequence can be found
                    currentSequence = ""
            else:
                currentSequence += line.strip("\n") #  strips out line breaks so that it is read correctly

    for item in matchingSequences:
        #  add the redundant motif-matching sequences to dataOutput.
        currentStructure.sequences.append(item)

    #  counts frequency positional of just matching sequences
    for item in set(matchingSequences): #  set() removes redundancy
        currentStructure.freqPositional[item[currentStructure.numResidues - currentStructure.searchPosition - 1]] += 1

    #  Counts frequency LastN from sequences list
    for item in set(sequences):
        for i in range(0, len(item)):
            currentStructure.freqLastN[item[i]] += 1

    #  prints "X sequences match the format: PX:XXXX PX:XXXX...."
    for k in currentStructure.freqAll:
        if currentStructure.freqAll[k] != 0 and sum(currentStructure.freqAll.values()) != 0 and sum(currentStructure.freqPositional.values()) != 0:
            currentStructure.enrichment[k] = round((currentStructure.freqPositional[k]/sum(currentStructure.freqPositional.values())) / (currentStructure.freqAll[k]/sum(currentStructure.freqAll.values())), 3)

    return currentStructure

