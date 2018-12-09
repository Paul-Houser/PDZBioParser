#  class that is used to store all relevant information about each file thats been parsed
class structure(object):
    def __init__(self):
        self.orgFile = ""
        self.organism = "" # holds fasta name
        self.numResidues = 0
        self.searchPosition = 0
        self.pList = []
        self.importantPositions = []
        self.sequences = [] #  holds the *redundant* sequences that also match the motifs.
        self.sequenceLabels = [] # labels for the above sequences from the fasta
        self.freqAllPsnl = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}
        self.freqLastN = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}
        self.freqMotifPositional  = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}
        self.freqAllPositional = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}
        # freqPositional is the same as freqAllPsnl but with redundancy removed
        self.freqnonRedMotifPositional  = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}
        self.freqnonRedAllPositional = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}
        self.enrichment = {"G":0,"A":0,"V":0,"L":0,"I":0,"M":0,"S":0,"C":0,"T":0,"P":0,"F":0,"Y":0,"W":0,"H":0,"K":0,"R":0,"D":0,"E":0,"N":0,"Q":0,"X":0,"U":0,"Z":0,"B":0,"O":0}

    # prints are for debugging purposes
    def printStructure(self):
        print("Organism: " + self.organism)
        print("numResidues: " + self.numResidues)
        print("searchPostion: " + self.numResidues)
        print("pList: " + self.pList)
        print("importantPositions: " + self.importantPositions)
    
    def printFrequencies(self):
        print("freqAllPsnl: " + self.freqAllPsnl)
        print("freqLastN: " + self.freqLastN)
        print("freqPositional: " + self.freqPositional)
        print("enrichment: " + self.enrichment)

