#  bioParser
#  Jordan Valgardson,Milo Rupp, Raiden van Bronkhorst, Paul Houser
#  12/8/2018

#  import dependencies
from dl import getFasta
from structure import structure
import time
import os
from  fileOutput import generateRawTSVFiles 
#  Interpret .fasta file
def read_file(currentStructure):
    #  returns false if the .fasta cannot be found.
    #  In main.py, if read_file returns false, the organism is added to an unfound organisms list.
    
    organismName = getFasta(currentStructure.organism, True)
    
    if not organismName:
        return False
    currentStructure.organism = organismName
    #  makes filename from organism name
    orgName = currentStructure.organism
    with open("~temp.file",'r') as f:
       with open(f.read(),'a') as f2:
           f2.write(" ".join([i for i in orgName.split('.')[0].split('_') if not i in set(['TaxID','R'])])+'\n')
       
   
   
    fileName = "fastas/" + orgName
    
    #  opens .fasta file to be parsed
    with open(fileName, "r") as file:

        lines = file.read()
        #generate a list of all proteins and headers,structure: [[header,protein],etc]
       
        proteins = []
        proteinsLastN = []
        # open fasta file and append sequences to a proteins and last N residues to last proteins last N
        for i in lines.split('\n>'):
            x = i.split('\n',1)
            if len(x[1])>currentStructure.numResidues:
                sequence = x[1].replace('\n','')
                proteins.append([x[0],sequence])
                proteinsLastN.append([x[0],sequence[-currentStructure.numResidues:]])
        # check if raw tsv organism files already exist if not make them
        if not os.path.isfile("rawTSV/" +currentStructure.organism.split(".")[0] + ".tsv"):
            generateRawTSVFiles(currentStructure.organism,proteinsLastN)
        # remove the proteins that dont match the given motif
        motifMatchingProteins = [[i[0],i[1]]  for i in proteinsLastN if all([i[1][-(1+currentStructure.pList[k])] in currentStructure.importantPositions[k] for k in range(len(currentStructure.pList))]) ]
        processFile(proteinsLastN,motifMatchingProteins,currentStructure)
        findEnrichment(currentStructure)
        return currentStructure
def processFile(proteinsLastN,motifMatchingProteins,currentStructure):
    # record the freq of each amino acid for all the proteins
    for protein in proteinsLastN:
        char =  protein[1][-(1+currentStructure.searchPosition)]
        currentStructure.freqAllPositional[char] += 1
    for protein in motifMatchingProteins:
        char =  protein [1][-(1+currentStructure.searchPosition)]
        currentStructure.freqMotifPositional[char] += 1
    # record the freq of each amino acid for all the non redundant proteins
    for protein in set(list(zip(*proteinsLastN))[1]):
        char = protein[-(1+currentStructure.searchPosition)]
        currentStructure.freqnonRedAllPositional[char] += 1
    LabelAndSequences = list(zip(*motifMatchingProteins)) # transpose the motifMatchingProteins list
    # record the freq of each amino acid for all the motif matching non redundant proteins
    
    for protein in set(LabelAndSequences[1]):
        char = protein[-(1+currentStructure.searchPosition)]
        currentStructure.freqnonRedAllPositional[char] += 1
   
    # save the redundant motif information to the current Structure
    currentStructure.sequences = LabelAndSequences[1]
    currentStructure.sequenceLabels = LabelAndSequences[0]
    return currentStructure

def findEnrichment(currentStructure):
    for k in currentStructure.freqAllPsnl:
        acidFreqAll = currentStructure.freqnonRedAllPositional[k]
        acidFreqPos = currentStructure.freqnonRedMotifPositional[k]
        sumFreqAll = sum(currentStructure.freqnonRedAllPositional.values())
        sumFreqPos = sum(currentStructure.freqnonRedMotifPositional.values())

        if acidFreqAll != 0 and sumFreqAll != 0 and sumFreqPos != 0:
            currentStructure.enrichment[k] = round((acidFreqPos / sumFreqPos) / (acidFreqAll / sumFreqAll), 3)
    
    

