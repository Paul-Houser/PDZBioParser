# PDZBioParser

## fasta files
You can download fasta files from [here.](http://www.uniprot.org/proteomes)

## Requirements
python 3
requests

## Usage
runInParallel.py [-h] [-c] 
                 file positions numResidues inputValues
                 [inputValues ...]

Arguments:
    file: a list of organisms to be parsed
    positions: The positions of interest (for multiple: 1,2,3,4 with no spaces)
    numResidues: The number of residues to provide statistics on
    inputValues: The motifs you want the proteins processed with.
                    ex: If you wanted to restrict your statistics to be on
                        proteins with the amino acids I,L,V,F at position 0,
                        and S,T at position 2, you would supply the input
                        values: P0:ILVF P2:ST
                        There is no limit to the number of motifs supplied.

Optional arguments:
    -h, --help      Show this help message and exit
    -c              Combine CSV files generated by runInParallel into a single
                    CSV for each position of interest supplied.

Example usage:
```
python3 organisms.txt 1,2,3 6 P0:ILVF P2:ST -c
```

BEFORE USE: update the file 'organisms_list.txt' to contain the names of all 
organisms to be parsed, each on their own line.

    ex.
        Homo sapiens
        Mus musculus
        Bos taurus
        Felis catus