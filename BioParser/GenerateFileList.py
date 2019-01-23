# parses input to setup files to call parse.py with
def parseFileNames(file):
    fileNames = []
    
    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            fileName = {'fileName':False,'taxonId':False,'R':False}
            orgName = []
            words = line.split()
            words = list(filter(None,words))
        
            for word in words:
                if word.isdigit():
                    fileName['taxonId'] = word
                elif word.lower() in set(['unreviewed','reviewed']):
                    fileName['R'] = word.lower()
                else:
                    
                    orgName.append(word)
            if not  fileName["R"]:
                fileName["R"] = 'unreviewed'
            if not fileName['taxonId']:
                fileName['taxonId'] = "temp"
            fileName["fileName"] = "_".join(orgName).replace('\n','')+'_'+"TaxID"+"_"+fileName["taxonId"]+"_"+"R_"+fileName["R"]+".fasta"
           
            fileNames.append(fileName["fileName"])
    return fileNames

def reviewedToAPI(x):
    reviewedToAPI = {"reviewed" : "yes", "unreviewed" : "no"}
    return reviewedToAPI[x]