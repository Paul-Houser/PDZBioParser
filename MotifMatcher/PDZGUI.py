# written by Michael Lee

# 12/28/2018

# This program takes the tsv folder and xml file as arguments and provides a GUI to search for
# proteins by match num, human sequence, other organism sequence, and Latin name

# very much a work in progress; the code is currently uncommented and badly needs to be cleaned up.
# This will happen in the next few days.

'''
PDZGUI0.4
python PDZGUI0.4.py -tsvFolder /path/folder -xmlFile /path/folder/filename.xml
'''

import tkinter as tk
import os
import xml.etree.ElementTree as ET
import argparse

class Backend:
    def __init__(self,all_seqs,organisms,root,matches_to_find,tsvs_loc,human_tsv,\
                 org_tsv=None,human_seq=None,org_seq=None,lat_name=None,\
                 console_print=None,file_write=None):
        if human_seq:
            hseq_location = all_seqs.index(human_seq)
            
        if lat_name:
            org_location = organisms.index(lat_name)
            tsv_address = tsvs_loc + "/" + org_tsv
        
        if human_seq and lat_name:
            sequences = self.sequences_from_xml(hseq_location,org_location,root,matches_to_find)
            human_matches = self.find_human_proteins_tsv(tsvs_loc,human_seq,human_tsv)
            org_matches = {i:[] for i in matches_to_find}
            for i in matches_to_find:
                org_matches[i] = self.find_org_protein(sequences[i],tsvs_loc,tsv_address)
            self.output(human_matches,org_matches,console_print,file_write,human_seq,org_seq,lat_name)
            
        elif org_seq and lat_name:
            org_matches = self.find_org_protein([org_seq],tsvs_loc,tsv_address)
            human_proteins = self.find_human_proteins_xml(tsvs_loc,human_tsv,matches_to_find,root,org_location,org_seq)
            human_matches = {i:[] for i in matches_to_find}
            for i in matches_to_find:
                human_matches[i] = self.find_human_proteins_tsv(tsvs_loc,human_proteins[i],human_tsv)
            self.output(human_matches,org_matches,console_print,file_write,human_seq,org_seq,lat_name)
            
        elif human_seq and org_seq:
            human_matches = self.find_human_proteins_tsv(tsvs_loc,human_seq,human_tsv)
            org_list = self.orgs_from_xml(hseq_location,org_seq,root,matches_to_find)
            org_matches = []
            orgs = []
            for item in os.listdir(tsvs_loc):
                for org in org_list:
                    if org in item.lower(): # .lower() is only necessary if filename has caps -- mine do, the repo ones don't
                        orgs.append(item)
            print(org_list)
            for tsv in orgs:
                tsv_address = tsvs_loc + "/" + tsv
                matches = self.find_org_protein([org_seq],tsvs_loc,tsv_address)
                org_matches.extend(matches)
            self.output(human_matches,org_matches,console_print,file_write,human_seq,org_seq,lat_name)

    def none_to_string(self,a_string):
        return a_string or ''

    def sequences_from_xml(self,hseq_location,org_location,root,matches_to_find):
        location = root[0][hseq_location][org_location]
        sequences = {i:self.none_to_string(location[6-i].text).split(",") for i in matches_to_find}
        return sequences

    def orgs_from_xml(self,hseq_location,org_seq,root,matches_to_find):
        ref_seq = root[0][hseq_location]
        org_list = []
        for nonRefOrganism in ref_seq:
            seqList = [self.none_to_string(nonRefOrganism[-i+6].text).split(",") for i in range(6,0,-1)]
            if org_seq in [item for sublist in seqList for item in sublist]:
                org_list.append(list(nonRefOrganism.attrib.values())[0][:-4].lower())
        return org_list

    def find_human_proteins_tsv(self,tsvs_loc,human_seq,human_tsv):
        protein_matches = []
        filename = tsvs_loc + "/" + human_tsv
        with open(filename,'r') as tsv_file:
            
            for line in tsv_file:
                if line.split("\t")[1].replace("\n","") in human_seq:
                    protein_matches.append(line)
        return protein_matches

    def find_human_proteins_xml(self,tsvs_loc,human_tsv,matches_to_find,root,org_location,org_seq):
        filename = tsvs_loc + "/" + human_tsv
        with open(filename,'r') as tsv_file:
            human_proteins = tsv_file.readlines()
        del human_proteins[0]
        match_dict = {i:[] for i in matches_to_find}
        for i in matches_to_find: ## USER-DEFINED
            for node in root[0]:
                proteins = self.none_to_string(node[org_location][-i+6].text).split(",") ## you'd better fix this line, Michael
                for k in proteins:
                    if k == org_seq:
                        match_dict[i].append(list(node.attrib.values())[0])
                        continue
        return match_dict

    def find_org_protein(self,org_seq_list,tsvs_loc,tsv_address):
        count=0
        protein_matches = []
        with open(tsv_address,'r') as tsv_file:
            org_seq_set = set(org_seq_list)
            for line in tsv_file:
                if line.replace("\n","").split("\t")[1] in org_seq_set:
                    protein_matches.append(line)
        return protein_matches

    def output(self,human_matches,org_matches,console_print,file_write,human_seq,org_seq,lat_name):
        to_output = "Human proteins matching the input criteria:\n"
        if type(human_matches) is list:
            human_matches_pretty = [(h.split("\t")[1].replace("\n",""),h.split("\t")[0]) for h in human_matches]
            for match in human_matches_pretty:
                to_output+=match[0]+"\t"+match[1]+"\n\n"
        elif type(human_matches) is dict:
            for match_num in human_matches:
                to_output+="{0} match:\n".format(match_num)
                human_matches_pretty = [(h.split("\t")[1].replace("\n",""),h.split("\t")[0]) for h in human_matches[match_num]]
                for match in human_matches_pretty:
                    to_output+=match[0]+"\t"+match[1]+"\n\n"
                if len(human_matches_pretty) == 0:
                    to_output+="[no matches]\n\n"
        to_output+="\n\nother proteins matching the input criteria:\n\n"
        if type(org_matches) is dict:
            for match_num in org_matches:
                to_output+="{0} matches:\n".format(match_num)
                org_matches_pretty = [(o.split("\t")[1].replace("\n",""),o.split("\t")[0]) for o in org_matches[match_num]]
                for org in org_matches_pretty:
                    to_output+=org[0]+"\t"+org[1]+"\n\n"
                if len(org_matches_pretty) == 0:
                    to_output+="[no matches]\n\n"
        elif type(org_matches) is list:
            org_matches_pretty = [(o.split("\t")[1].replace("\n",""),o.split("\t")[0]) for o in org_matches]
            for match in org_matches_pretty:
                to_output+=match[0]+"\t"+match[1]+"\n\n"
        to_output+="\n\n--end of data printout--"
        if console_print:
            print(to_output)
        if file_write:
            file_name = "{0} {1} {2}.txt".format(human_seq,org_seq,lat_name[:-4])
            with open(file_name,'w') as file_object:
                file_object.write(to_output)
                print("--task completed--")



class GUI:
    def __init__(self, master,human_tsv,tsvs_loc,xml_loc):
    
        # drawing window
        self.var6 = tk.IntVar()
        self.var5 = tk.IntVar()
        self.var4 = tk.IntVar()
        self.var3 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var1 = tk.IntVar()
        self.file_write = tk.IntVar()
        self.console_print = tk.IntVar()
        
        self.master = master
        master.title("protein retrieval tool")

        self.instructions = tk.Label(master, text="""Fill data into two of the following\
 three boxes and select
 "write to file" or "print to console".

 If you provide a Latin name, it's fine if you just put in the first
 few letters (but be unambiguous!)""")
        self.instructions.grid(columnspan=8,sticky=tk.W)

        self.human_seq_label = tk.Label(master, text="Human sequence:")
        self.human_seq_label.grid(columnspan=5,sticky = tk.W)

        self.org_seq_label = tk.Label(master, text="other org sequence:   ")
        self.org_seq_label.grid(columnspan=5,sticky = tk.W)

        self.lat_name_label = tk.Label(master,text="Lat. name:")
        self.lat_name_label.grid(columnspan=3,sticky=tk.W)

        self.human_entry = tk.Entry(master,width=15)
        self.human_entry.grid(columnspan=4,row=1,column=4,sticky=tk.W)

        self.org_entry = tk.Entry(master,width=15)
        self.org_entry.grid(columnspan=4,row=2,column=4,sticky=tk.W)

        self.lat_entry = tk.Entry(master,width=30)
        self.lat_entry.grid(columnspan=7,row=3,column=4)

        self.button6 = tk.Checkbutton(master,text="6",variable=self.var6)
        self.button6.grid(row=4,column=0)
        self.button6.select()

        self.button5 = tk.Checkbutton(master,text="5",variable=self.var5)
        self.button5.grid(row=4,column=1)
        self.button5.select()

        self.button4 = tk.Checkbutton(master,text="4",variable=self.var4)
        self.button4.grid(row=4,column=2)
        self.button4.select()

        self.button3 = tk.Checkbutton(master,text="3",variable=self.var3)
        self.button3.grid(row=4,column=3)

        self.button2 = tk.Checkbutton(master,text="2",variable=self.var2)
        self.button2.grid(row=4,column=4)

        self.button1 = tk.Checkbutton(master,text="1",variable=self.var1)
        self.button1.grid(row=4,column=5)

        self.match_label = tk.Label(master, text="matches")
        self.match_label.grid(row=4,column=6)

        self.file_write_button = tk.Checkbutton(master,text="write to file",variable=self.file_write)
        self.file_write_button.grid(columnspan=3,row=5)

        self.console_print_button = tk.Checkbutton(master,text="print to console",variable=self.console_print)
        self.console_print_button.grid(columnspan=3,column=3,row=5)
        self.console_print_button.select()

        # find tsv and xml files
        self.human_tsv =human_tsv
        self.tsvs_loc = tsvs_loc 
        self.xml_loc  = xml_loc
        
        # does tsv folder exist?
        if os.path.exists(tsvs_loc):
            pass
        else:
            raise FileNotFoundError("TSV folder does not exist!")
            
        # parse xml file
        root,all_seqs,organisms = self.parse_xml(xml_loc)

        # submit button
        self.submit = tk.Button(master,text="submit",command=lambda:self.get_entries_and_run(organisms,tsvs_loc,human_tsv,all_seqs,root))
        self.submit.grid(columnspan=6,row=7)



    def parse_xml(self,xml_loc):
        tree = ET.parse(xml_loc)
        root = tree.getroot()
        all_seqs = [list(child.attrib.values())[0] for child in root[0]]
        
        # starting with summary, we now have a list of the (nonhuman) organisms.
        organisms = list(root[0].attrib.values())[0].split(";")
        organisms = [item.split(",") for item in organisms]
        organisms = [organisms[x][0] for x in range(1,len(organisms))] # start with 1 because homo_sapiens is in position 0
        return root,all_seqs,organisms

    def get_entries_and_run(self,organisms,tsvs_loc,human_tsv,all_seqs,root):
        self.human_seq = self.human_entry.get()
        self.org_seq = self.org_entry.get()
        self.lat_name = self.lat_entry.get()
        self.lat_name = self.lat_name.lower().strip().replace(" ","_")
        if len(self.lat_name)!=0:
            org_tsv = [file for file in os.listdir(tsvs_loc) if self.lat_name.lower() in file.lower()][0]
            self.lat_name = [org for org in organisms if self.lat_name in org.lower()]
        matches_to_find = []
        print_to_console,write_to_file = [bool(val) for val in [self.console_print.get(),self.file_write.get()]]
        if not print_to_console and not write_to_file:
            raise RuntimeError("No output method specified!")
        button_data = [self.var6.get(),self.var5.get(),self.var4.get(),self.var3.get(),self.var2.get(),self.var1.get()]
        for i in range(6):
            if button_data[i] == 1:
                matches_to_find.append(-i+6)
        if self.check_for_valid():
            if self.human_seq != "" and self.lat_name != "":
                computation = Backend(all_seqs,organisms,root,matches_to_find,tsvs_loc,human_tsv,\
                                      org_tsv,self.human_seq,lat_name=self.lat_name,\
                                      console_print=print_to_console,file_write=write_to_file)
            elif self.org_seq != "" and self.lat_name != "":
                computation = Backend(all_seqs,organisms,root,matches_to_find,tsvs_loc,human_tsv,\
                                      org_tsv,org_seq=self.org_seq,lat_name=self.lat_name,console_print=print_to_console,\
                                      file_write=write_to_file)
            elif self.human_seq != "" and self.org_seq != "":
                computation = Backend(all_seqs,organisms,root,matches_to_find,tsvs_loc,human_tsv,\
                                      human_seq=self.human_seq,org_seq=self.org_seq,\
                                      console_print=print_to_console,file_write=write_to_file)
            else:
                raise RuntimeError("Invalid input!")
        else:
            raise RuntimeError("Invalid input!")


    def check_for_valid(self):
        amino_acids = ["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]
        humanSeqOk = -1
        orgSeqOk = -1
        latNameOk = -1
        if len(self.human_seq) == 6 and all(x.upper() in amino_acids for x in self.human_seq):
            humanSeqOk = True
            self.human_seq = self.human_seq.upper()
        elif self.human_seq == "":
            pass
        else:
            humanSeqOk = False
        if len(self.org_seq) == 6 and all(x.upper() in amino_acids for x in self.org_seq):
            orgSeqOk = True
            self.org_seq = self.org_seq.upper()
        elif self.org_seq == "":
            pass
        else:
            orgSeqOk = False
        if len(self.lat_name) == 1:
            self.lat_name = self.lat_name[0]
            latNameOk = True
        elif self.lat_name=="":
            pass
        else:
            latNameOk = False
        if all([humanSeqOk,orgSeqOk,latNameOk]):
            if sum([humanSeqOk,orgSeqOk,latNameOk])==1:# 1+1-1 == 1
                return True
            else:
                raise RuntimeError("Make sure that exactly two boxes are filled!")
        else:
            print([humanSeqOk,orgSeqOk,latNameOk])
            raise ValueError("Make sure to enter only acceptable characters.")

def parseArgs():
    parser = argparse.ArgumentParser(description="protein retrieval")
    parser.add_argument('-tsvFolder',required=True,type=str,
                        help="Provide address of folder with tsv files.\
Usage: /path/folder")
    parser.add_argument('-xmlFile',required=True,type=str,
                        help="Provide address of xml file.\
Usage: /path/folder/file.xml")
    return parser.parse_args()

if __name__ == "__main__":
    args=parseArgs()
    tsvs_loc=os.path.normpath(args.tsvFolder)
    xml_loc=os.path.normpath(args.xmlFile)
    refOrg = "homo_sapiens_TaxID_9606_R_yes.tsv"
    source = tk.Tk()
    source.geometry("350x240")
    source.grid_rowconfigure(7,minsize=40)
    protein_gui = GUI(source, refOrg, tsvs_loc, xml_loc)
    source.mainloop()
