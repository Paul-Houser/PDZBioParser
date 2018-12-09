import argparse
import sys
import motifFileMaker
import motifCounterXMLParse
import os
def parseArgs():
    parser = argparse.ArgumentParser(
        description='TODO')
    parser.add_arguement('-refOrganism', required=True, type=str,
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
    start = time.clock()
    folderName = os.path.basename(os.path.normpath(args.sequenceFolder.split('/')))
    motifName = args.inputValues.replace(" ",'-')
    motif = {(5-k[0]):k[1] for k in[i.split(':') for i in args.inputValues.split('P')]}
    xmlFileName = folderName + "_"+motifName+".xml"
    tsvFileName = folderName + "_"+motifName+".tsv"
    motifFileMaker.motif_Finder(folderName,motif,xmlFileName)
    motifCounterXMLParse.generateOutput(xmlFileName,tsvFileName)
    
