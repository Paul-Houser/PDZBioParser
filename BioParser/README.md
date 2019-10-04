# BioParser
## Program Description
BioParser is a tool used to process C-terminal decameric sequences, with the evaluation of PDZ binding domains as is primary goal. BioParser will filter and analyze the proteomes of as many organisms as are supplied to it, and will filter based off as many motifs as are supplied to it.

Motifs refers to specifying specific amino acids at certain positions. For example, if you wanted to analyze the enrichment of the amino acids S and T at position 2, you could supply the -motifs argument with ``` P2:ST ```

BioParser also creates detailed data on the proteomes that is stored in the CSV folder that is created during the programs execution. The -c argument combines all CSV's for one organism, which can be usefull when large numbers of positions are being processed.

## Package Requirements
```
python3
requests == 2.20.1
numpy == 1.15.4     --- required if generating heat maps
matplotlib == 3.0.2 --- required if generating heat maps
```

It is recommended that the user run MotifAnalyzer-PDZ.py within a virtual environment. 
The steps to start up a virtual environment are listed below. The requirements.txt included
contains all required python3 packages to be downloaded within the virtual environment.

Virtual Environment Setup:
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
usage: MotifAnalyzer-PDZ.py [-h] -organisms ORGANISMS -positions POSITIONS
                            -numResidues NUMRESIDUES
                            [-motifs MOTIFS [MOTIFS ...]] [-c] [-heatmaps]
                            [-motifID MOTIFID]

Run C-terminal decameric sequence processing on many files simultaneously

optional arguments:
  -h, --help            show this help message and exit
  -organisms ORGANISMS  The text file containing latin names of organisms.
                        (e.g. organisms.txt)
  -positions POSITIONS  The positions to search over, delimited with commas.
                        (e.g. 1,3,4,5)
  -numResidues NUMRESIDUES
                        The number of residues to provide statistics on.
                        (e.g. 6)
  -motifs MOTIFS [MOTIFS ...]
                        The matching positions with desired amino acids. 
                        (e.g. P0:ILVF P2:ST ... PX:X)
  -c                    Add this flag to create combined CSVs.
  -heatmaps             Add this flag to make enrichment heat maps for csv data.
  -motifID MOTIFID      If heat maps are created, use this naming convention.
                        [default=motif]
```

```
Example usage:
python3 MotifAnalyzer-PDZ.py -organisms organisms.txt -positions 1,3 -numResidues 6 -motifs P0:I P2:ST
```

The organism text file should contain the names of all organisms to be parsed, the taxon id and whether it is reviewed or unreviewed.

General Structure:
```
Organism_Name TaxonID Reviewed
```

Example:
```
Homo_sapiens 9606 reviewed
gallus_gallus 9031 unreviewed
```

## Program Flow
User calls MotifAnalyzer-PDZ.py
MotifAnalyzer-PDZ.py calls functions from fileOutput.py -- parseFileNames, makeFolders, writeSummaryFile, as well as setUpHandler.py.
setUpHandler.py calls functions from fileOutput.py -- writeCSV and writeSequenceLists., as well as readFile from parse.py.
readFile calls getFasta from dl, and writeRawTSV from fileOutput
#### MotifAnalyzer-PDZ.py:

  - First calls are to parseArgs and checkInput. These just make sure the arguments entered by the user are valid, and exits the program if they aren't.
  - From fileOutput.py, makeFolders is called. This creates the necessary directories for the results to be stored in. These directories are 'csv', 'fastas', 'sequenceLists', and 'rawTSV'.
  - From fileOutput.py, parseFileNames is called. This takes the organism names and information from the user provided text file, and generates the name for each fasta that will be downloaded.
  - distributeWork is called, which starts multiple threads to analyze the proteomes, so that more than one can be processed at once. distributeWork calls setupHandler.py.
  - Once distributeWork has finished executing, writeSummaryFile from fileOutput.py is called. writeSummaryFile generates a summary file containing organism names, numbers of motif matching proteins, and total number of proteins for each organism.
  - createHeatmaps is called. This takes the csv files that were generated, and calls extractCSV.py, as well as createHeatMap.py.
  - if the -c flag was provided by the user, combineData is called. This creates the combinedCSV directory and reads in the data from the separate csv files.

#### setUpHandler.py:

  - The arguments provided by the call from distributeWork in MotifAnalyzer-PDZ.py are parsed.
  - getImportantPositions is called. This takes the motif arguments provided and extracts the positions and their associated amino acids. Returns a list of lists. for example, P0:ILVF and P2:ST returns ```[[0, I, L, V, F], [2, S, T]]```
  - setUpStructure is called. This Creates the structure object containing the organism, number of residues, given position, and the motif information. it uses readFile from parse.py to do this. It also Calculates and writes the output to the csv file, tsv file, and unfoundOrganisms.txt. (unfoundOrganisms.txt is generated if it doesn't already exist).


## Program Output

### csv


### sequenceLists


### rawTSV


### combinedCSVs


### unfoundOrganisms.txt


### summaryFile.csv


## Heat Maps
Create heat maps displaying the enrichment values and optional statistical annotations.
Can be run with MotifAnalyzer-PDZ.py by supplying the `-heatmaps` flag.
If running from MotifAnalyzer-PDZ.py, the user has the option to supply a naming convention 
for the generated files with the `-motifID` argument.

Example usage:
```
python3 MotifAnalyzer-PDZ.py -organisms organisms.txt -positions 1,3 -numResidues 6 -motifs P0:I P2:ST -heatmaps -motifID my_motif
```

