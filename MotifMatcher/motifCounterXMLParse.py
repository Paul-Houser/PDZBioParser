from operator import mul
from lxml import etree as ET
from functools import reduce
import math as m

from scipy.stats import hypergeom
import itertools as it
import numpy as np

from scipy import integrate
import pylandau

r"main.py -refOrganism bos -sequenceFolder C:\Users\jordan\Downloads\PDZBioParser-master(1)\PDZBioParser-master\BioParser\fastas -numResidues 6 -motifs p0:W p1:W p3:W p4:W -out test1 -significance 0.999 -full"
# functions necessary to calculate the expected proportion for each level of matching
def hyperGeomParams(motif,length):

    
    N= reduce(mul,motif)
    motif = [i-1 for i in motif]
    results = [1]*(length+1)
    for i in range(1,length+1):
        results[i] = sum([reduce(mul,i) for i in it.combinations(motif,i)])
    return N,results

def nCr(n, r):
    # n choose r mathematical function
    r = min(r, n-r)
    num = reduce(mul, range(n, n-r, -1), 1)
    den = reduce(mul, range(1, r+1), 1)
    return num / den

def calcExpected(n,a,PValues):
    z = normal_CDF_inverse(a)

    return [[P + z*(P*(1-P)/n)**0.5 , P - z*(P*(1-P)/n)**0.5] for P in PValues]
def calcPValues(n,N1,params,P_actu):


    assert sum(PValues) >= 1-(7./3 - 4./3 -1)**0.5
    for num in range(len(PValues)):
        if PValues[num] == 0:
            assert P_actu[num] == 0

    return [hypergeom.sf(P_actu[i], N1,params[i],n) +0.5*hypergeom.pmf(P_actu[i], N1,params[i],n) for i in range(len(PValues))]


# functions that interpret the resulsts of the xml file generate by motif file maker and return a tsv file

def MotifToIndex(motif):
    return [len(motif[k]) for k in motif]



def probCalcV2(pos,length):
    posProb = [0]*(length+1)

    for n in range(2**length):
        probString = "{0:b}".format(n)
        probString = "0"*(length - len(probString)) + probString
        probType = sum([int(x) for x in probString])
        temp = 1
        for k in range(length):
            
            
            top = (pos[k]-1)**int(probString[k])
            
            temp *= top/(pos[k])
            if temp == 0:
                break
        
        posProb[probType] += temp
        
    return posProb




def findMotifs(fileName,numResidues):
    """Parses the xml output of motif file maker and generate a dictionary that has a list of the counts
    for the number of matches for each sequence"""
    matchSet =  set(["match"+str(x) for x in range(numResidues,0,-1)])
    organismSet = set()
    motifRuningSum = {}
    score = []
    with open(fileName,'rb') as f:
        tree = ET.iterparse(f,events=("start", "end"))
        
        for event,element in tree:

            if element.tag in matchSet and event == "end":
                if element.text:
                    score.append(len(element.text.split(",")))
                else:
                    score.append(0)
            elif  element.tag == "RefSequence"  and event == "start":
                refSequenceKey = element.attrib['name']
                motifRuningSum[refSequenceKey] = []
                
            elif element.tag == "NonRefOrganism" and event == "end":
                motifRuningSum[refSequenceKey] .append({element.attrib['name']:score})

                score = []
            elif element.tag == "Summary":
                motifRuningSumAndProteinTotals = element.attrib['name']
                proteinTotals = [protein.split(',') for protein in motifRuningSumAndProteinTotals.split(";")]
                proteinTotals = {prot[0]:int(prot[1]) for prot in proteinTotals}
                organismSet = set(x for x in proteinTotals)
        
        return motifRuningSum,motifRuningSumAndProteinTotals

def creatTSV(motifRuningSumAndProteinTotals, outFile,motif, numResidues,significance):
    # generates the tsv file output summarizing the xml file generated by motif file maker
    # it unpacks the motifRuningSum dicitionary and makes a table
    motifRuningSum = motifRuningSumAndProteinTotals[0]
    organismsTotals = motifRuningSumAndProteinTotals[1].split(";")
    proteinTotals = [protein.split(',') for protein in motifRuningSumAndProteinTotals[1].split(";")]
    proteinTotals = {prot[0]:int(prot[1]) for prot in proteinTotals}
    refOrg = organismsTotals[0]

    posList = MotifToIndex(motif)
    posList = posList + [20]*(numResidues-len(posList))
    N1, params = hyperGeomParams(posList,numResidues)

    sigRegion = {org:calcExpected(proteinTotals[org], significance, PValues) for org in proteinTotals}
    
    with open(outFile,'w') as proportionTest:
        with open(outFile.split(".")[0]+"ChiSquare.tsv","w") as chiSquareFile:
            # make header of the file
            recordOrder = []
            proportionTest.write(refOrg)
            chiSquareFile.write(refOrg)
            for refSequence , organisms in motifRuningSum.items():
                proportionTest.write('\t')
                chiSquareFile.write("\t")
                for organismAndMatches in organisms:
                    for organism in organismAndMatches:
                        recordOrder.append(organism)
                        proportionTest.write(organism+'\t')
                        chiSquareFile.write(organism+'\t')
                proportionTest.write('\n')
                chiSquareFile.write("\n")
                break
            proportionTest.write("Total Motif counts:")
            for organisms in recordOrder:
                proportionTest.write('\t')
                chiSquareFile.write("\t")
                proportionTest.write(str(proteinTotals[organisms]))
                chiSquareFile.write(str(proteinTotals[organisms]))
            proportionTest.write('\n')
            chiSquareFile.write("\n")
            # fill in the remainder of the table
            for refSequence , organisms in motifRuningSum.items():
                proportionTest.write(refSequence+'\t')
                chiSquareFile.write(refSequence+'\t')
                for organismAndMatches in organisms:
                
                    for organism in organismAndMatches:
                       
                        PV = [x for x in calcStanDev(proteinTotals[organism],N1,params ,np.array(organismAndMatches[organism]+[proteinTotals[organism]-sum(organismAndMatches[organism])]))]
                        #harmonic mean of P values

                        lengthP = len(PV)
                        HMP = 1/sum([((1/lengthP)/p)for p in PV])

                        loc = c*(m.log(numResidues+1)+ 0.874)
                        sca = 2/m.pi
                        TrueP,err = integrate.quad(pylandau.get_landau_pdf, 1/HMP, 1000, args=(loc, sca))

                        chiSquareFile.write(str(TrueP))

                        for matchNum in range(len(organismAndMatches[organism])):
                            
                            if sigRegion[organism][matchNum][0] < organismAndMatches[organism][matchNum]/proteinTotals[organism]:
                                 proportionTest.write(str(organismAndMatches[organism][matchNum])+'+'+',')
                            elif sigRegion[organism][matchNum][1] > organismAndMatches[organism][matchNum]/proteinTotals[organism]:
                                proportionTest.write(str(organismAndMatches[organism][matchNum])+'-'+',')
                            else:
                               proportionTest.write(str(organismAndMatches[organism][matchNum])+',')
                    proportionTest.write('\t')
                    chiSquareFile.write("\t")
                
                proportionTest.write('\n')
                chiSquareFile.write("\n")

 
def generateOutput(fileName,outFile,motif,numResidues,significance):
    creatTSV(findMotifs(fileName,numResidues),outFile,motif,numResidues,significance)
