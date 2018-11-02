import requests
import os

# downloads missing files from uniprot, call with fasta name
# example: getFasta("homo_sapiens.fasta")


def getFasta(org, silent):
    original = org
    if not os.path.isfile("fastas/" + org):
        if not silent:
            print("File not found, downloading...")
        org = org.split(".")[0]
        org = org.replace("_", "+AND+")
        # url = "http://www.uniprot.org/uniprot/?query=reviewed:yes+AND+" + org + "+AND+reference:yes&sort=score&format=fasta&compress=no"
        searchUrl = "https://www.uniprot.org/proteomes/?sort=score&desc=&compress=no&query=" + \
            org + "+NOT+taxonomy:viruses&fil=reference:yes&format=list"

        s = requests.get(searchUrl, allow_redirects=True, stream=True)
        protId = str(s.content).split("\\n")[0].split("'")[1]
        if len(protId) < 10:
            return False
        url = "https://www.uniprot.org/uniprot/?query=proteome:" + protId + "&compress=no&format=fasta&reviewed:no"

        r = requests.get(url, allow_redirects=True, stream=True)

        if len(str(r.content)) < 10:
            if not silent:
                print(original + " is not on uniprot!")
            return False
        else:
            open("fastas/" + org.replace("+AND+", "_") +
                 ".fasta", 'wb').write(r.content)
            return True
    return True