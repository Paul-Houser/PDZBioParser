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


## Heat Maps
Create heat maps displaying the enrichment values and optional statistical annotations.
Can be run with MotifAnalyzer-PDZ.py by supplying the `-heatmaps` flag or separately.
If running from MotifAnalyzer-PDZ.py, the user has the option to supply a naming convention 
for the generated files with the `-motifID` argument.

### Running from MotifAnalyzer-PDZ
Example usage:
```
python3 MotifAnalyzer-PDZ.py -organisms organisms.txt -positions 1,3 -numResidues 6 -motifs P0:I P2:ST -heatmaps -motifID my_motif
```

### Running Otherwise
First run extractCSV.py to read in data formatted with MotifAnalyzer-PDZ.py.
```
usage: extractCSV.py [-h] --files FILES [-outfile OUTFILE]
                     [-headerlines HEADERLINES]

optional arguments:
  -h, --help            show this help message and exit
  --files FILES         Path to csv files to read in. (e.g. 'csv/*.csv')
  -outfile OUTFILE      File to write condensed enrichment CSV information to
                        [default=model.p].
  -headerlines HEADERLINES
                        Number of header lines to skip over [default=5].
```

Example usage:
```
python3 extractCSV.py --files 'csv/*.csv' -outfile model.p
```

Once extractCSV.py has run, then run createHeatMap.py to create and save heatmaps.

```
usage: createHeatMap.py [-h] --enrichment ENRICHMENT [-organisms ORGANISMS]
                        [-annotation ANNOTATION] [-thresh THRESH]
                        [-title TITLE] --out OUT
optional arguments:
  -h, --help            show this help message and exit
  --enrichment ENRICHMENT
                        Pickle file to read enrichment values from.
  -organisms ORGANISMS  Ordered organisms to use in plot.
  -annotation ANNOTATION
                        Pickle file containing the statistically significant
                        values
  -thresh THRESH        Threshold value to for the annotations of the plot.
  -title TITLE          Title for plot.
  --out OUT             png file to write plot to.
```

Example usage:
```
python3 createHeatMap.py --enrichment model_motif1/position1.p --out m1_p1.png
```
