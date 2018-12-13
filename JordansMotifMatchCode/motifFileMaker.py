import os
import xml.etree.cElementTree as ET
import lxml.etree as etree
#written by Jordan Valgardson

def motif_Finder(inTSVFolder,motif_type,outFile,refOrganism):
    allEndings = {}
    motifEndings = {}
    writeFile = open(outFile,"wb")
    refEndings = set()
    for file in os.listdir(inTSVFolder):
        readFile = open(inTSVFolder + file, 'r')
        allEndings[file] = set()
        for line in readFile:
            tempSequence = line.split('\t')[1].replace('\n','')
            if len(tempSequence) == 6:
                allEndings[file].add(tempSequence)
    for organism in allEndings:
        
        
        motifEndings[organism] = set()
        for motif in allEndings[organism]:
           
            if all(motif[key] in motif_type[key] for key in motif_type):
                 motifEndings[organism].add(motif)
            
    refEndings = refEndings | motifEndings[refOrganism]
    del motifEndings[refOrganism]
    root = etree.Element("root")
    for Ref_motif in refEndings:
        refEnding  = etree.SubElement(root, "RefSequence",name = Ref_motif)
        
        
        for organism in motifEndings:
            tempDict = {6:set(),5:set(),4:set(),3:set(),2:set(),1:set()}
            for motif in motifEndings[organism]:
                score = sum([1 if motif[i] == Ref_motif[i] else 0 for i in [5,4,3,2,1,0]])
                if score != 0:
                    tempDict[score].add(motif)




            NonRefOrganism = etree.SubElement(refEnding, "NonRefOrganism",name = organism)
            
            for score in range(6,0,-1):
                matchScore = etree.SubElement(NonRefOrganism, "match"+str(score)).text = ",".join(tempDict[score])
    tree = etree.ElementTree(root)
    writeFile.write(etree.tostring(tree, pretty_print=True))
    writeFile.close()
    



        
        
    
    
