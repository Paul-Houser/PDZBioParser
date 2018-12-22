from operator import mul
from lxml import etree as ET
from functools import reduce
import math as m

# functions necessary to calculate the expected proportion for each level of matching
def normal(x):
    return (1/(2*m.pi)**0.5 )* m.e**(-(x**2)/2)
def rational_approx(t):
    a = [2.515517, 0.802853, 0.010328]
    b = [1.432788, 0.189269, 0.001308]
    num= (a[2]*t + a[1])*t + a[0]
    den = ((b[2]*t + b[1])*t + b[0])*t + 1
    return t - num/ den
 
def normal_CDF_inverse(p):
    if p < 0.5:
        return -rational_approx( m.sqrt(-2*m.log(p)) )
    else:
        return rational_approx( m.sqrt(-2*m.log(1-p)) )
def nCr(n, r):
    r = min(r, n-r)
    num = reduce(mul, range(n, n-r, -1), 1)
    den = reduce(mul, range(1, r+1), 1)
    return num / den
def getComb(motif,numResidues):
    nonMotif = numResidues-len(motif)
    motif =[len(motif[x]) for x in motif]
    radx = [motif.count(x) for x in sorted(set(motif))]+[nonMotif]
    chance = [1/x for x in sorted(set(motif))]+[1/20]
    comb = [0]*len(radx)
    allComb =[]
    radxValue =[1]+ [0]*(len(radx)-1)
    for x in range(1,len(radx)):
            radxValue[x] = sum([radxValue[i]*radx[i] for i in range(x)])+1
    for num in range( reduce (mul,[j+1 for j in radx])):
        for x in range(len(radx)-1,-1,-1):
            num1 = num//radxValue[x]
            comb[x] = num1
            num -= num1*radxValue[x]
        allComb.append(comb)
        comb = [0]*len(radx)
    return allComb,chance,radx
def getPValue(allComb,chance,radx):
    PValues = [0]*(1+sum(radx))
    allCombDict = {x:[] for x in range(0,1+sum(radx))}
    for x in allComb:
        allCombDict[sum(x)].append(x)
    for x in allCombDict:
        PValues[x] = sum([reduce(mul,[(chance[i]**j[i])*((1-chance[i])**(radx[i]-j[i]))*nCr(radx[i],radx[i]-j[i]) for i in range(len(radx))]) for j in allCombDict[x]])
    return PValues
def calcExpected(n,a,PValues):
    z = normal_CDF_inverse(a)
    
    return [[P + z*(P*(1-P)/n)**0.5 , P - z*(P*(1-P)/n)**0.5] for P in PValues]
def calcStanDev(n,PValues,P_actu):

    return [(P_actu[i]/n-PValues[i])/((PValues[i]*(1-PValues[i])/n)**0.5) for i in range(len(PValues))]
"""
# functions that interpret the resulsts of the xml file generate by motif file maker and return a tsv file
def findMotifs(fileName):
  #  #Parses the xml output of motif file maker and generate a dictionary that has a list of the counts
  #  for the number of matches for each sequenc
    motifRuningSum = {}
    tree = ET.parse(fileName)
    root = tree.getroot()
    # iterates through the reference sequences in the file
    for summary in root:
        proteinTotals = summary.attrib['name']
        for refSequence in summary:
            
            refSequenceKey = refSequence.attrib['name']
            motifRuningSum[refSequenceKey] = []
            # iterate through the organisms for the given reference sequence
            for organism in refSequence :
                score = []
                # iterate through the matching sequences for the organism for the given reference sequence
                for matchscore in organism:
                    # if there are matches count them if not append 0 to the score list
                    if matchscore.text:
                        score.append(len(matchscore.text.split(",")))
                    else:
                        score.append(0)
                
                motifRuningSum[refSequenceKey] .append({organism.attrib['name']:score})
    return motifRuningSum,proteinTotals
    """
# functions that interpret the resulsts of the xml file generate by motif file maker and return a tsv file
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
    allComb,chance,radx = getComb(motif,numResidues)
    PValues = list(reversed(getPValue(allComb,chance,radx)))
    sigRegion = {org:list(reversed(calcExpected(proteinTotals[org], significance, PValues))) for org in proteinTotals}
    
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
                        chiSquareFile.write(str(-2*sum([m.log(0.5*max(min(m.erfc(-x/(2**0.5)),m.erfc(x/(2**0.5))),7./3 - 4./3 -1)) for x in calcStanDev(proteinTotals[organism],PValues[:-1] ,organismAndMatches[organism])])))             
                        
                        proportionTest.write(str(sum([((organismAndMatches[organism][x] -proteinTotals[organism]*PValues[x])**2)/proteinTotals[organism]*PValues[x] for x in range(len(PValues[:-1]))])))
                        proportionTest.write(str(calcStanDev(proteinTotals[organism],PValues[:-1] ,organismAndMatches[organism]))[1:-1])
                
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
