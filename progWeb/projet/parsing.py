#from models import Genome, gene_prot
import os

chemin = "./data/"#./data"
listObjet = os.listdir(chemin)
print(listObjet)
#for file in listObjet:
#print( "cds" in listObjet[3])

for file in listObjet:
    if "cds" in file :
        #print("cds")
        espece = file.split("_cds")[0]
        #print(espece)
        ### CDS
        #for ligne in open(chemin+file):   
        #    if ligne.startswith('>'):
        #        print(ligne) 
        ### Pep
        print(chemin+espece+"_pep.fa")
        for ligne in open(chemin+espece+"_pep.fa"):   
            if ligne.startswith('>'):
                #print(ligne) 
                nom_transcrit = ligne.split(" ")[0][1:]
                id_genome = ligne.split(" ")[2].split(":")[1]
                print(id_genome)
                start_pos = ligne.split(" ")[2].split(":")[3]
                end_pos = ligne.split(" ")[2].split(":")[4]

                if len(ligne.split(" "))>3:
                    description = ligne.split("description:")[1]
                    print(description) 

                #else: 
                #    description = None
                #else:
                #des
                #print(description)
                #print(start_pos)
                #print(end_pos)
                print("\n")
                #print(nom_transcrit)
