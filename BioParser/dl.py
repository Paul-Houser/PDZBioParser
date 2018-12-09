import requests
import os
from structure import structure
# downloads missing files from uniprot, call with fasta name
# example: getFasta("homo_sapiens.fasta",yes,True,taxonId=9606)


def getFasta(org,silent):
    original = org
    taxonId = False
    if not os.path.isfile("fastas/" + org):
        if not silent:
            print("File not found, downloading...")
        # I implemented reviewed verse unreviewed genome grabing but it is an unelegant solution, come back later and fix this
        fullFile = org.split("TaxID")
  
        taxAndReview = fullFile[1].split(".")[0].split("_")
       
        if taxAndReview[1] != 'temp':
            taxonId = taxAndReview[1]
        reviewed = taxAndReview[3]
        if not taxonId:
            org = org.split("_TaxID")[0]
            
       
            org = org.replace("_", "+AND+")
            # url = "http://www.uniprot.org/uniprot/?query=reviewed:yes+AND+" + org + "+AND+reference:yes&sort=score&format=fasta&compress=no"
            searchUrl = "https://www.uniprot.org/taxonomy/?sort=score&desc=&compress=no&query=" + \
                org + "&fil=reference:yes&format=list"
    
            s = requests.get(searchUrl, allow_redirects=True, stream=True)
            taxonId = str(s.content).split("\\n")[0].split("'")[1]
            original = original.replace("TaxID_temp","TaxID_"+str(taxonId))
            if os.path.isfile("fastas/" + original):
                return original
        url = "https://www.uniprot.org/uniprot/?query=reviewed:"+reviewed+"+AND+organism:"+taxonId+"&format=fasta&compress=no"
        
        r = requests.get(url, allow_redirects=True, stream=True)

        if len(str(r.content)) < 10:
            if not silent:
                print(original + " is not on uniprot!")
            return False
        else:
            open("fastas/" + original, 'wb').write(r.content)
            return original
    
    return original

