import os
import xml.etree.cElementTree as ET
import lxml.etree as etree
#written by Jordan Valgardson

def motif_Finder(inTSVFolder,motif_type,outFile):
    allEndings = {}
    motifEndings = {}
    writeFile = open(outFile,"wb")
    humanEndings = set()
    for file in os.listdir(inTSVFolder):
        readFile = open(inTSVFolder + file, 'r')
        allEndings[file] = set()
        for line in readFile:
            if len(line.split('\t')[0]) == 6:
                allEndings[file].add(line.split('\t')[0])
    for organism in allEndings:
        motifEndings[organism] = set()
        for motif in allEndings[organism]:
           
            if all(motif[key] in motif_type[key] for key in motif_type):
                 motifEndings[organism].add(motif)
            
    humanEndings = humanEndings | motifEndings["Homo_sapiens.tsv"]
    del motifEndings["Homo_sapiens.tsv"]
    root = etree.Element("root")
    for Human_motif in humanEndings:
        humanEnding  = etree.SubElement(root, "humanSequence",name = Human_motif)
        
        
        for organism in motifEndings:
            tempDict = {6:set(),5:set(),4:set(),3:set(),2:set(),1:set()}
            for motif in motifEndings[organism]:
                score = sum([1 if motif[i] == Human_motif[i] else 0 for i in [5,4,3,2,1,0]])
                if score != 0:
                    tempDict[score].add(motif)




            NonHumanOrganism = etree.SubElement(humanEnding, "NonHumanOrganism",name = organism)
            
            for score in range(6,0,-1):
                matchScore = etree.SubElement(NonHumanOrganism, "match"+str(score)).text = ",".join(tempDict[score])
    tree = etree.ElementTree(root)
    writeFile.write(etree.tostring(tree, pretty_print=True))
    writeFile.close()
    


motif_Finder(TSVFolder,motif_2,File1)
                
        
        
    
    
