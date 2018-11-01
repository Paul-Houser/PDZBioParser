#!/bin/bash

positions="1 3 4 5"

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment

mkdir visuals
mkdir -p model_motif1/csv model_motif1/sequenceLists
mkdir -p model_motif2/csv model_motif2/sequenceLists
mkdir -p model_motif3/csv model_motif3/sequenceLists

# MOTIF ONE
m1_0="P0:ILVF"
m1_2="P2:ST"

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment/bioParser
for p in $positions
do
    python runInParallel.py all.txt $p 6 $m1_0 $m1_2
done

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment
mv bioParser/csv model_motif1/
mv bioParser/sequenceLists model_motif1/

mkdir bioParser/csv bioParser/sequenceLists

for p in $positions
do
    python extractCSV.py --files "model_motif1/csv/*$p.csv" -outfile model_motif1/position$p.p
    python createHeatMap.py --enrichment model_motif1/position$p.p --out model_motif1/m1_p$p.png -title "Enrichments: Motif 1, Position $p" -organisms ordered_organisms.txt 
    cp model_motif1/m1_p$p.png visuals/
done

# MOTIF TWO
m2_0="P0:AFILMVWY"
m2_2="P2:ST"

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment/bioParser
for p in $positions
do
    python runInParallel.py all.txt $p 6 $m2_0 $m2_2
done

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment
mv bioParser/csv model_motif2/
mv bioParser/sequenceLists model_motif2/

mkdir bioParser/csv bioParser/sequenceLists

for p in $positions
do
    python extractCSV.py --files "model_motif2/csv/*$p.csv" -outfile model_motif2/position$p.p
    python createHeatMap.py --enrichment model_motif2/position$p.p --out model_motif2/m2_p$p.png -title "Enrichments: Motif 2, Position $p" -organisms ordered_organisms.txt
    cp model_motif2/m2_p$p.png visuals/
done

# MOTIF THREE
m3_0="P0:AFILMVWY"
m3_2="P2:AFILMVWY"

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment/bioParser
for p in $positions
do
    python runInParallel.py all.txt $p 6 $m3_0 $m3_2
done

cd /home/cosbeyr/CSCI474/enrichment/project6_enrichment
mv bioParser/csv model_motif3/
mv bioParser/sequenceLists model_motif3/

mkdir bioParser/csv bioParser/sequenceLists

for p in $positions
do
    python extractCSV.py --files "model_motif3/csv/*$p.csv" -outfile model_motif3/position$p.p
    python createHeatMap.py --enrichment model_motif3/position$p.p --out model_motif3/m3_p$p.png -title "Enrichments: Motif 3, Position $p" -organisms ordered_organisms.txt
    cp model_motif3/m3_p$p.png visuals/
done
