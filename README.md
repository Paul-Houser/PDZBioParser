# PDZBioParser

## fasta files
You can download fasta files from [here.](http://www.uniprot.org/proteomes)

## Requirements
python 3,
lxml,
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
python3 runInParallel.py -organisms all_organisms.txt -inputValues P0:WYIAfLVM P2:ST -positions 1,3,5 -numResidues 6

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
