import operator
from lxml import etree as ET


def findMotifs(fileName):
    motif3 = open(fileName,'r')
    motifRuningSum = {}
    tree = ET.parse(fileName)
    root = tree.getroot()
    for humanSequence in root:
        runningSumKey = humanSequence.attrib['name']
        motifRuningSum[runningSumKey] = []
        for organism in humanSequence :
            score = []
            for matchscore in organism:
                
                if matchscore.text:
                    score.append(len(matchscore.text.split(",")))
        
                else:
                    score.append(0)
            motifRuningSum[runningSumKey] .append({organism.attrib['name']:score})
    return motifRuningSum

def creatTSV(motifRuningSum, outFile):
    with open(outFile,'w') as writeFile:
        for humanSequence , organism in motifRuningSum.items():
            writeFile.write('\t')
            for key in organism:
                for motif in key:
                    writeFile.write(motif+'\t')
            writeFile.write('\n')
            break
        for humanSequence , organism in motifRuningSum.items():
            writeFile.write(humanSequence+'\t')
            for key in organism:
                for motif in key:
                    writeFile.write(str(key[motif])[1:-1]+ "\t")
            writeFile.write('\n')
        
def generateOutput(fileName,outFile):
    creatCSV(findMotifs(fileName),outFile)
