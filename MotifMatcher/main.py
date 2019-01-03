import argparse
import sys
import motifFileMaker
import motifCounterXMLParse
import os
import time
import makeXMLWrapper
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
    parser.add_argument('-numResidues', required=True, type=int, 
                        help='The number of residues to provide statistics on. Usage: 6')
    parser.add_argument('-inputValues', required=True,nargs='+',
                        help='The matching positions with desired amino acids. Usage: P0:ILVF P2:ST ... PX:X')
    parser.add_argument('-out', required=True, type=str,
                        help='out put file directory')
    parser.add_argument('-significance', required=True, type=float,
                        help='significance cut off value example 0.95 corresponds to P<0.05 or 5% chance the item was flagged in error')
    parser.add_argument("-decouple", action='store_true',required = False, default = False,
                        help = "If a xml file has all ready been generated use  this flag to skip xml generation")
    return parser.parse_args()
if __name__ == "__main__":
    args = parseArgs()
    start = time.clock()
    folderName = os.path.normpath(args.sequenceFolder)
    motifName ='-'.join(args.inputValues).replace(':','_')
    motif = {(5-int(k[0])):set(list(k[1])) for k in[i.replace('P','').split(':') for i in args.inputValues]}
    xmlFileName = args.out +".xml"
    tsvFileName = args.out +".tsv"
    if args.decouple:
        motifCounterXMLParse.generateOutput(xmlFileName,tsvFileName,motif,args.numResidues,args.significance)
    else:
        # get the operating system
        OpSys = sys.platform
        print(OpSys)
        input()
        # decide whether to using the makeXML or the python motifFileMaker
        if OpSys in ["win32","linux"]:
            makeXMLWrapper.callMakeXML(folderName+'/',motif,args.numResidues,xmlFileName,args.refOrganism)
        else:
            motifFileMaker.motif_Finder(folderName+'/',motif,args.numResidues,xmlFileName,args.refOrganism)
        motifCounterXMLParse.generateOutput(xmlFileName,tsvFileName,motif,args.numResidues,args.significance)
    print("completed in: " +str(time.clock()-start))
    
