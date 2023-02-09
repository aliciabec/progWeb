from projet.models import Genome, Gene_prot, Annotation, Utilisateur
import os

chemin = "./projet/data/"#test/"
listObjet = os.listdir(chemin)

dicoGene = {}
dicoGenome = {}
listNonAnnote = []
for file in listObjet:
    if "cds" in file :

        espece = file.split("_cds")[0]
        seq = "" 
        id_genome = ""
        for ligne in open(chemin+espece+".fa"):  
            
            if not ligne.startswith('>'):
                seq = seq + ligne.strip("\n")
            else: 
                id_genome = ligne.split("chromosome:")[1].split(":")[0]
                
        dicoGenome[id_genome]=[seq, len(seq), espece]
        dicoGene[id_genome]= {}
        print(len(seq))
        seq = ""
        nom_transcrit = ""
        NomGene = None
        description = None
        start_pos = 0
        end_pos = 0
        seqNucleotidique = ""
        for ligne in open(chemin+espece+"_pep.fa"):  
            
            if ligne.startswith('>'):
                nom_transcrit = ""
                NomGene = None
                description = None
                start_pos = 0
                end_pos = 0
                
                nom_transcrit = ligne.split(" ")[0][1:]

                start_pos = ligne.split(" ")[2].split(":")[3]
                end_pos = ligne.split(" ")[2].split(":")[4].strip("\n")

                if len(ligne.split(" "))>3:
                    NomGene = ligne.split("gene:")[1].split(" ")[0]
                    description = ligne.split("description:")[1].strip("\n")
                elif id_genome not in listNonAnnote:
                    listNonAnnote.append(id_genome)    
                seq = ""
                

            else: 
                seq = seq + ligne.strip("\n")
                dicoGene[id_genome][nom_transcrit]=[start_pos, end_pos, NomGene, description, seq, seqNucleotidique]

        nom_transcrit = ""
        for ligne in open(chemin+espece+"_cds.fa"):  
            if ligne.startswith('>'):
                nom_transcrit = ""
                nom_transcrit = ligne.split(" ")[0][1:]
                seq = ""
            else: 
                seq = seq + ligne.strip("\n")
                dicoGene[id_genome][nom_transcrit][5]=seq 

for idGenome in dicoGene.keys():
    G = Genome(Id_genome = idGenome, taille_sequence = dicoGenome[idGenome][1],
    sequence_genome = dicoGenome[idGenome][0], espece = dicoGenome[idGenome][2])
    G.save()
    for nomTranscrit in dicoGene[idGenome].keys():
        Gene_prot(nom_transcrit= nomTranscrit, Id_genome = Genome.objects.get(Id_genome=idGenome), nom_gene = dicoGene[idGenome][nomTranscrit][2]
        ,start_position= dicoGene[idGenome][nomTranscrit][0], end_position= dicoGene[idGenome][nomTranscrit][1] 
        , description = dicoGene[idGenome][nomTranscrit][3], sequence_nucleotidique= dicoGene[idGenome][nomTranscrit][5] 
        ,sequence_peptidique = dicoGene[idGenome][nomTranscrit][4]).save(force_insert=True)

for i in listNonAnnote:
    Annotation(Id_genome = Genome.objects.get(Id_genome=i)).save(force_insert=True)
