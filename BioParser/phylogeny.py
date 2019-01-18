from ete3 import NCBITaxa

def order_orgs(org_list):
    org_dict = {}
    for item in org_list:
        org_dict[int(item.split("_")[3])] = item
    ncbi = NCBITaxa()
    
    tree = ncbi.get_topology(org_dict.keys())
    # print(tree.get_ascii(attributes=['sci_name','rank']))

    organisms = []
    for node in tree.traverse("postorder"):
        if node.rank == 'species':
            organisms.append(org_dict[node.taxid])

    return organisms,tree.get_ascii(attributes=['sci_name','rank'])
