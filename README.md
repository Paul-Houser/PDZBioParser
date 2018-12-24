# PDZBioParser
# BioParser
## fasta files
You can download fasta files from [here.](http://www.uniprot.org/proteomes)

## Requirements
python 3,
requests,
numpy,
matplotlib,
## Usage
```
runInParallel.py [-h] -organisms ORGANISMS -positions POSITIONS
                        -numResidues NUMRESIDUES
                        [-inputValues INPUTVALUES [INPUTVALUES ...]] [-c]
                        [-heatmaps] [-motifID MOTIFID]

Arguments:
  -organisms ORGANISMS  The text file containing latin names of organisms.
                        Usage: all.txt
  -positions POSITIONS  The positions to search over, delimited with commas.
                        Usage: 1,3,4,5
  -numResidues NUMRESIDUES
                        The number of residues to provide statistics on.
                        Usage: 6
  -inputValues INPUTVALUES [INPUTVALUES ...]
                        The matching positions with desired amino acids.
                        Usage: P0:ILVF P2:ST ... PX:X



Optional arguments:
  -c                    Add this flag to create combined CSVs.
  -heatmaps             Add this flag to make enrichment heat maps for csv
                        data.
  -motifID MOTIFID      If heatmaps are created, use this naming convention.
                        Usage: motif1
Example usage:
Linux:
python3 runInParallel.py -organisms all_organisms.txt -motifs P0:WYIAfLVM P2:ST -positions 1,3,5 -numResidues 6
Windows 10:
runInParallel.py -organisms all_organisms.txt -numResidues 6 -motifs P0:WIYAFLVM P2:ST -positions 1,3,5

```

BEFORE USE: update the file 'organisms_list.txt' to contain the names of all 
organisms to be parsed, each on their own line. 
General Structure:
```
Name TaxonID Reviewed/Unreviewed

Example.
bos taurus 9913 no
caenorhabditis elegans 6239 no
escherichia coli 83333 yes
homo sapiens 9606 yes
```
# MotifMatcher
# Reqirements
Python3,
lxml,
# Usage
```
main.py [-h] -refOrganism REFORGANISM -sequenceFolder SEQUENCEFOLDER
               -numResidues NUMRESIDUES -inputValues INPUTVALUES
               [INPUTVALUES ...] -out OUT -significance SIGNIFICANCE
Arguments:
               
   -refOrganism REFORGANISM
                        Provide the file name of the organism that the other
                        organisms will be compared with. Usage:
                        /path/folder/organism.tsv
  -sequenceFolder SEQUENCEFOLDER
                        The path of the folder that contains tsv files that
                        contain the last N many residues of all the proteins
                        in the proteomes in question. Usage: /path/folder
  -numResidues NUMRESIDUES
                        The number of residues to provide statistics on.
                        Usage: 6
  -inputValues INPUTVALUES [INPUTVALUES ...]
                        The matching positions with desired amino acids.
                        Usage: P0:ILVF P2:ST ... PX:X
  -out OUT              Output file directory and name. Do not include file
                        extensions. Usage: /path/folder/fileName_motif_example
  -significance SIGNIFICANCE
                        significance cut off value example 0.9999 corresponds
                        to P<0.0001 or 0.1 percent chance the item was flagged
                        in error
Example Usage:
python3 main.py -refOrganism homo_sapiens_TaxID_9606_R_yes.tsv -sequenceFolder rawTSV/ -numResidues 6 -inputValues P0:WYIAFLVM P2:ST -out motif_2_human -significance 0.9999
```
