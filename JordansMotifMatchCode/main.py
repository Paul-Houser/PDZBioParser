import argparse
import sys
import motifFileMaker
import motifCounterXMLParse
import os
import time
def parseArgs():
    parser = argparse.ArgumentParser(
        description='TODO')
    parser.add_argument('-refOrganism', required=True, type=str,
                         help = "Provide the file name of the organism that the other organisms will \
                            be compared with. Usage: /path/folder/organism.tsv")
    parser.add_argument('-sequenceFolder',required=True, type=str,
                        help="The path of the folder that contains tsv files that \
                        contain the last N many residues of all the proteins in the proteomes in question.\
                        Usage: /path/folder")
    parser.add_argument('-inputValues', required=True,nargs='+',
        help='The matching positions with desired amino acids. Usage: P0:ILVF P2:ST ... PX:X')
    return parser.parse_args()
if __name__ == "__main__":
    args = parseArgs()
    print(args)
    start = time.clock()
    folderName = os.path.basename(os.path.normpath(args.sequenceFolder))
    print(args.inputValues)
    motifName ='-'.join(args.inputValues).replace(':','_')
    motif = {(5-int(k[0])):set(list(k[1])) for k in[i.replace('P','').split(':') for i in args.inputValues]}
    xmlFileName = folderName + "_"+motifName+".xml"
    tsvFileName = folderName + "_"+motifName+".tsv"
    motifFileMaker.motif_Finder(folderName+'/',motif,xmlFileName,args.refOrganism)
    motifCounterXMLParse.generateOutput(xmlFileName,tsvFileName)
    
