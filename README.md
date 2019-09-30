# PDZBioParser
# BioParser
## fasta files
You can download fasta files from [here.](http://www.uniprot.org/proteomes)

## Requirements
python 3,
requests,
numpy,
matplotlib

## Program Description
BioParser is a tool used to process C-terminal decameric sequences, with the evaluation of PDZ binding domains as is primary goal. BioParser will filter and analyze the proteomes of as many organisms as are supplied to it, and will filter based off as many motifs as are supplied to it.

Motifs refers to specifying specific amino acids at certain positions. For example, if you wanted to analyze the enrichment of the amino acids S and T at position 2, you could supply the -motifs argument with ``` P2:ST ```

BioParser also creates detailed data on the proteomes that is stored in the CSV folder that is created during the programs execution. The -c argument combines all CSV's for one organism, which can be usefull when large numbers of positions are being processed.



## Usage
```
usage: main.py [-h] -organisms ORGANISMS -positions POSITIONS -numResidues
               NUMRESIDUES [-motifs MOTIFS [MOTIFS ...]] [-c] [-heatmaps]
               [-motifID MOTIFID]

Run C-terminal decameric sequence processing on many files simultaneously

optional arguments:
  -h, --help            show this help message and exit
  -organisms ORGANISMS  The text file containing latin names of organisms.
                        Usage: all.txt
  -positions POSITIONS  The positions to search over, delimited with commas.
                        Usage: 1,3,4,5
  -numResidues NUMRESIDUES
                        The number of residues to provide statistics on.
                        Usage: 6
  -motifs MOTIFS [MOTIFS ...]
                        The matching positions with desired amino acids.
                        Usage: P0:ILVF P2:ST ... PX:X
  -c                    Add this flag to create combined CSVs.
  -heatmaps             Add this flag to make enrichment heat maps for csv
                        data.
  -motifID MOTIFID      If heatmaps are created, use this naming convention.
                        Usage: motif1
Example usage:
Linux:
python3 main.py -organisms all_organisms.txt -motifs P0:WYIAfLVM P2:ST -positions 1,3,5 -numResidues 6

Windows 10:
python3 main.py -organisms all_organisms.txt -motifs P0:WIYAFLVM P2:ST -positions 1,3,5-numResidues 6

```

BEFORE USE: update the file 'organisms_list.txt' to contain the names of all 
organisms to be parsed, each on their own line. 
General Structure:
```
Name TaxonID Reviewed/Unreviewed

Example.
bos taurus 9913 unreviewed
caenorhabditis elegans 6239 unreviewed
escherichia coli 83333 reviewed
homo sapiens 9606 reviewed
```
# MotifMatcher
# Reqirements
Python3,
lxml
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
  -decouple             If a xml file has all ready been generated use this
                        flag to skip xml generation
  -pyth                 force the use of motifFileMaker over makeXML. Using
                        this flag will slowdown exicution.
  -GUI                  Launch GUI automatically after program exicution.

     
Example Usage:
Linux
python3 main.py -refOrganism homo_sapiens_TaxID_9606_R_reviewed.tsv -sequenceFolder rawTSV/ -numResidues 6 -inputValues P0:WYIAFLVM P2:ST -out motif_2_human -significance 0.9999
Windows
main.py -refOrganism homo_sapiens_TaxID_9606_R_reviewed.tsv -sequenceFolder rawTSV/ -numResidues 6 -inputValues P0:WYIAFLVM P2:ST -out motif_2_human -significance 0.9999

```
