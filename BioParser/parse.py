#  bioParser
#  Milo Rupp, Raiden van Bronkhorst, Paul Houser
#  10/12/17

#  import dependencies
from dl import getFasta
from structure import structure

#  matchingSequences holds the last numResidues residues from each sequence that match the given motif
matchingSequences = []

#  sequences holds the last numResidues residues of every sequence
sequences = []

currentSequence = "" # the current chunk of amino acids
currentLabel = ""
sequenceLabel = ""


#  Interpret .fasta file
def read_file(currentStructure):
    global currentSequence

    #  returns false if the .fasta cannot be found.
    #  In main.py, if read_file returns false, the organism is added to an unfound organisms list.
    if not getFasta(currentStructure.organism, True):
        return False
    
    #  makes filename from organism name
    orgName = currentStructure.organism
    fileName = "fastas/" + orgName

    #  opens .fasta file to be parsed
    with open(fileName, "r") as file:

        lines = file.readlines()
        lines.append(">")

        for line in lines:
            
            # a '>' signifies the start of a new protein in the fasta files
            if line[0] == ">":
                newProtein(line, currentStructure)
            else:
                #  strips out linebreaks from sequence and add them to currentSequence
                currentSequence += line.strip("\n")
    
    # adds the motif-matching sequences to currentStructure (redundancy NOT removed)
    addMatching(currentStructure)

    # counts frequency positional of just matching sequences and adds them to currentStructure (redundancy removed)
    countMatchingPsnl(currentStructure)

    # counts frequency in last N residues and adds them to currentStructure (redundancy removed)
    countLastN(currentStructure)

    # finds enrichment values for each position and adds them to currentStructure
    findEnrichment(currentStructure)

    return currentStructure


# set up variables for starting a new protein
def newProtein(line, currentStructure):
    #  This function modifies the global variables sequenceLabel, currentLabel, and currentSequence
    global sequenceLabel
    global currentLabel
    global currentSequence

    sequenceLabel = currentLabel
    currentLabel = line

    # if currentSequence != an empty string, then a full sequence has been found and can be processed
    if currentSequence != "":
        processSequence(currentStructure)
    
    # Reset currentSequence in preparation for the next sequence
    currentSequence = ""


# processesSequence takes a complete sequence and processes it based on the importantPositions list in currentStructure
def processSequence(currentStructure):
    global currentSequence
    global sequences
    global matchingSequences
    
    for char in currentSequence:
        currentStructure.freqAll[char] += 1
    
    # sets currentSequence to equal the last numResidues of itself
    currentSequence = currentSequence[-currentStructure.numResidues:] 
    sequences.append(currentSequence)

    # Determines if the sequence matches motif in currentStructure.importantPositions
    shouldAppend = True
    for i in range(0, len(currentStructure.pList)):
         if not currentSequence[len(currentSequence) - currentStructure.pList[i] - 1] in currentStructure.importantPositions[i]:
             shouldAppend = False
             break
    
    # If the sequence matches the motif, append sequence to matchingSequences, and sequenceLabel to
    # currentStructure.sequenceLabels.
    if shouldAppend:
        matchingSequences.append(currentSequence)
        currentStructure.sequenceLabels.append(sequenceLabel)


def addMatching(currentStructure):
    for item in matchingSequences:
        currentStructure.sequences.append(item)


def countMatchingPsnl(currentStructure):
    for item in set(matchingSequences): # set removes redundancy
        aminoAcid = item[currentStructure.numResidues - currentStructure.searchPosition - 1]
        currentStructure.freqPositional[aminoAcid] += 1


def countLastN(currentStructure):
    for item in set(sequences):
        for i in range(0, len(item)):
            currentStructure.freqLastN[item[i]] += 1


def findEnrichment(currentStructure):
    for k in currentStructure.freqAll:
        acidFreqAll = currentStructure.freqAll[k]
        acidFreqPos = currentStructure.freqPositional[k]
        sumFreqAll = sum(currentStructure.freqAll.values())
        sumFreqPos = sum(currentStructure.freqPositional.values())

        if acidFreqAll != 0 and sumFreqAll != 0 and sumFreqPos != 0:
            currentStructure.enrichment[k] = round((acidFreqPos / sumFreqPos) / (acidFreqAll / sumFreqAll), 3)
