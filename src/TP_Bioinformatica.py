import string
import random
import xml.etree.cElementTree as ET
import pymol
import __main__
from pymol import cmd
from random import randint
from Bio.Blast import NCBIWWW 
from Bio.Blast import NCBIXML
from Bio.PDB import PDBList
from modeller import *
from modeller.automodel import *
from Bio.Align.Applications import ClustalwCommandline
from Bio.Align.Applications import MSAProbsCommandline
from Bio import AlignIO
#import tmalign
#from tkinter import *
'''
from Bio.Seq import Seq
from Bio import Align 

aligner = Align.PairwiseAligner()
aligner.match_score 

aligner.mismatch_score

score = aligner.score("ACGT","ACAT")
print(score)

aligner.match_score = 1.0
aligner.mismatch_score = -2.0
aligner.gap_score = -2.5
score = aligner.score("ACGT","ACAT")
print(score)
'''

sec1 = 'AGEKGKKIFVQKCSQCHTVCSQCHTVEKGGKHKTGPNEKGKKIFVQKCSQCHTVLHGLFGRKTGQA'
sec2 = 'GTTATAATATTGCTAAAATTATTCAGAGTAATATTGTGGATTAAAGCCACAATAAGATTTATAATCTTAAATGATGGGACTACCATCCTTACTCTCTCCATTTCAAGGCTGACGATAAGGAGACCTGCTTTGCCGAGGAGGTACTACAGTTCTCTTCACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTTTTAATATGTCCAGTATTCATTTTTGCATGTTTGGTTAGGCTAGGGCTTAGGGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTAGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTCTATTGTGCCATACTGTTGAATGTTTATAATGCATGTTCTGTTTCCAAATTTCATGAAATCAAAACATTAATTTATTTAAACATTTACTTGAAATGTTCACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTTTTAATATGTCCAGTATTCATTTTTGCATGTTTGGTTAGGCTAGGGCTTAGGGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTAGATTTATATATCAAAGGAGGCT'
sec3 = 'ACTTTGTTTTTATCTCCTGCTCTATTGTGCCATACTGTTGAATGTTTATACCCTACATGGTGCATGTTCTGTTTCCAAATTTCATGAAATCAAAACATTAATTTATTTAAACATTTACTTGAAATGTTCACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTTTTAATATGTCCAGTATTCATTTTTGCATGTTTGGTTAGGCTAGGGCTTAGGGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTAGATTTATATATCAAAGGAGGCT'
sec4 = 'AAUCAUGUAGUAGGCUUUUUUUUAGAUCAUGCU'
sec5 = 'GCUUAUCCUGCUUUGGCUCUGGCGUAUUAACUGGCU'
sec6 = 'GCUUAGUAUCCUGCUUUGGCUCUGGCGUAUUAACUA'
sec7 = 'AGDVEKGKKIFIMK' #Proteina
sec8 = 'ATTGGACGTAATGC' #ADN
sec9 = 'AGGUACCGAUCCA'  #ARN
sec10 = 'ACUT'  #proteina
sec11 = 'ACT'

secuencias = {
    'CitC_humano':'AGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA',
    'CitC_gorila':'AGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA',
    'CitC_pollo' :'AGDIEKGKKIFVQKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA'
}
 
diccionario_ARN = {
    "UUU":"F", "UUC":"F", "UUA":"L", "UUG":"L", "CUU":"L", "CUC":"L", "CUA":"L", "CUG":"L",
    "AUU":"I", "AUC":"I", "AUA":"I", "AUG":"M", "GUU":"V", "GUC":"V", "GUA":"V", "GUG":"V",
    "UCU":"S", "UCC":"S", "UCA":"S", "UCG":"S", "CCU":"P", "CCC":"P", "CCA":"P", "CCG":"P",
    "ACU":"T", "ACC":"T", "ACA":"T", "ACG":"T", "GCU":"A", "GCC":"A", "GCA":"A", "GCG":"A",
    "UAU":"Y", "UAC":"Y", "UAA":"X", "UAG":"X", "CAU":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
    "AAU":"N", "AAC":"N", "AAA":"K", "AAG":"K", "GAU":"D", "GAC":"D", "GAA":"E", "GAG":"E",
    "UGU":"C", "UGC":"C", "UGA":"X", "UGG":"W", "CGU":"R", "CGC":"R", "CGA":"R", "CGG":"R",
    "AGU":"S", "AGC":"S", "AGA":"R", "AGG":"R", "GGU":"G", "GGC":"G", "GGA":"G", "GGG":"G"
}

diccionario_ADN = {
    "TTT":"F", "TTC":"F", "TTA":"L", "TTG":"L", "CTT":"L", "CTC":"L", "CTA":"L", "CTG":"L",
    "ATT":"I", "ATC":"I", "ATA":"I", "ATG":"M", "GTT":"V", "GTC":"V", "GTA":"V", "GTG":"V",
    "TCT":"S", "TCC":"S", "TCA":"S", "TCG":"S", "CCT":"P", "CCC":"P", "CCA":"P", "CCG":"P",
    "ACT":"T", "ACC":"T", "ACA":"T", "ACG":"T", "GCT":"A", "GCC":"A", "GCA":"A", "GCG":"A",
    "TAT":"Y", "TAC":"Y", "TAA":"X", "TAG":"X", "CAT":"H", "CAC":"H", "CAA":"Q", "CAG":"Q",
    "AAT":"N", "AAC":"N", "AAA":"K", "AAG":"K", "GAT":"D", "GAC":"D", "GAA":"E", "GAG":"E",
    "TGT":"C", "TGC":"C", "TGA":"X", "TGG":"W", "CGT":"R", "CGC":"R", "CGA":"R", "CGG":"R",
    "AGT":"S", "AGC":"S", "AGA":"R", "AGG":"R", "GGT":"G", "GGC":"G", "GGA":"G", "GGG":"G"
}

def pasar_a_lista(cadena): 
    lista = []
    for char in cadena:
        lista.append(char)

    return lista 

def dividir_3(cadena):
    lista_nueva = []
    for i in range(0, len(cadena), 3):
        lista_nueva.append(cadena[i:i+3])

    return lista_nueva          

def stop(cadena_mutada): 
    lista = dividir_3(cadena_mutada)
    cadena_corta = ""

    for i in lista:
        if((i=='UAA') or (i=='UAG') or (i=='UGA') or (i=='TAA') or (i=='TAG') or (i=='TGA')):
            longitud = lista.index(i)
            return cadena_corta.join(lista[:longitud])
    
    return cadena_mutada

def sin_duplicados(sec):
    lista_nueva = []
    for i in sec:
        if i not in lista_nueva:
            lista_nueva.append(i)
    return lista_nueva   
  
def es_adn(sec):
    return sec.count("A") & sec.count("C") & sec.count("G") & sec.count("T") 

def es_arn(sec):
    return sec.count("A") & sec.count("C") & sec.count("G") & sec.count("U") 

def que_es(lista):
    secuencia = sin_duplicados(lista)

    if(len(secuencia)>=4 and (not es_adn(secuencia)) and (not es_arn(secuencia))):
        #print("La secuencia " + lista + ": es una proteina") 
        return "proteina" 
    elif(es_adn(secuencia)):
        #print("La secuencia " + lista + ": es un ADN")  
        return "ADN" 
    elif(es_arn(secuencia)):
        #print("La secuencia " + lista + ": es un ARN")  
        return "ARN" 
    else:
        #print("La secuencia " + lista + ": es una proteina")  
        return "proteina"         

def hay_stop(secuencia):
    lista = dividir_3(secuencia)
    res = False
    stops = ['UAA', 'UAG', 'UGA', 'TAA' , 'TAG', 'TGA']

    for i in stops:
        if i in lista[:-1]:
            res = True
    return res

def validar_fasta(secuencia):
    sec = que_es(secuencia)
    resultado = False

    if(hay_stop(secuencia)):
        print("El archivo fasta es incorrecto, hay un stop dentro de la secuencia")
        return resultado
    elif(sec=="proteina"):
        print("El archivo fasta es una proteina, ingrese una secuencia de ADN o ARN")
        return resultado
    elif(len(secuencia)%3 !=0):
        print("El tamaño de la secuencia no es el correcto")
        return resultado
    else:
        return True    

def obtener_secuencia(fasta):
    try:
        sec_fasta = open(fasta)          
        lista = []
        cadena_final = ""

        for line in sec_fasta:
            if line[0] != '>':
                lista.append(line.strip())
        
        sec_fasta.close()
        return cadena_final.join(lista)       
    except:
        return "El archivo no existe" # No sale este print cuando no existe el archivo ???????

# PREC: No puede ser una secuencia de una proteina
def pasar_a_proteina(secuencia): 
    cadena = dividir_3(secuencia)
    cadena_nueva = []
    cadena_ARN = ""
    adn_o_arn = que_es(secuencia)
    dic_adn = diccionario_ADN.items()
    dic_arn = diccionario_ARN.items()

    if adn_o_arn == "ADN":
        for letras in cadena:
            for k,v in dic_adn:
                if(k.count(letras)):  
                    cadena_nueva.append(v)
    elif adn_o_arn == "ARN":
        for letras in cadena:
            for k,v in dic_arn:
                if(k.count(letras)):  
                    cadena_nueva.append(v)

    return cadena_ARN.join(cadena_nueva)                      

def mutar_manual(peptido, index, letra):
    cadena_ADN = pasar_a_lista(peptido)
    cadena_mutada = ""

    cadena_ADN.insert(index,letra)
    del cadena_ADN[index+1]
    
    cadena_mut = cadena_mutada.join(cadena_ADN)
    cadena_final = stop(cadena_mutada.join(cadena_ADN))
    print("Secuencia original: " + peptido)
    print("Secuencia mutada:   " + cadena_mut)
    print("Secuencia final:    " + cadena_final)
    
    return cadena_final

def mutar_automatica(sec_fasta): 
    cadena_ADN = pasar_a_lista(sec_fasta)
    cadena_mutada = ""
    quees = que_es(sec_fasta)
    randPos = randint(0,(len(sec_fasta)-1))
    
    if(quees == "ADN"): 
        randLetra = random.choice("ACGT") 
        cadena_ADN.insert(randPos,randLetra)
        print("Mutó la letra: " + randLetra + " en la posición: " + str(randPos+1))
        
    elif(quees == "ARN"):
        randLetra = random.choice("ACGU") 
        cadena_ADN.insert(randPos,randLetra)
        print("Mutó la letra: " + randLetra + " en la posición: " + str(randPos+1))
    
    del cadena_ADN[randPos+1]
    
    cadena_mut = cadena_mutada.join(cadena_ADN)
    cadena_final = stop(cadena_mutada.join(cadena_ADN))
    print("Secuencia original: " + sec_fasta)
    print("Secuencia mutada:   " + cadena_mut)
    print("Secuencia final:    " + cadena_final)

    return cadena_final

def mutar_secuencia(sec, mut_letra): 
    try:
        if(mut_letra == 'M'):
            letra = input("Ingrese la letra del aminoácido en el que va a mutar: ").upper()
            index = int(input("Ingrese la posición: "))
            if(index > len(sec)):
                return print("Ingresó una posición fuera de rango, ingrese un número menor a: " + str(len(sec)))
            else:    
                return mutar_manual(sec, (index-1), letra)
        
        elif(mut_letra == 'A'):
            return mutar_automatica(sec) 

        else: 
            return print("La letra que eligió no es la correcta, debe elegir 'M' o 'A'")
    except:
        return print("Debe ingresar un número")

def blast_proteina_namePdb(seq_proteina, sec_a_analizar): 
    res = "La proteina no existe en la base de datos PDB"
    resultBlast = NCBIWWW.qblast(program= "blastp", database= "pdb", sequence= seq_proteina)
    blast = sec_a_analizar + ".xml"

    save_clk = open(blast, "w")
    save_clk.write(resultBlast.read())    
    save_clk.close()
    
    blast_records = NCBIXML.parse(open(blast))

    myScore = 0
    for blast_record in blast_records:
        for description in blast_record.descriptions:
            if(description.score > myScore):
                myScore = description.score
                res = description.accession
    return res

def buscaryGuardarPdb(nombreArc): 
    pdbdownload = PDBList()
    pdbdownload.retrieve_pdb_file(nombreArc, file_format="pdb")
    #falta seleccionar particion

def guardarEnFastaSeqMutada(mutacion):
    save_clk = open("mutacion.fasta", "w")
    #nombre generico
    save_clk.write(">CR457033.1 Homo sapiens "+'\n')  
    save_clk.write(mutacion)
    save_clk.close()

    original = open("CR457033.fasta", "r").read()
    save_clk2 = open("mutacion.fasta", "a")
    save_clk2.write('\n'+original)
    save_clk2.close()

def programa():

    sec_a_analizar = input("Ingrese el nombre del archivo FASTA que desea analizar: ")
    sec_fasta = obtener_secuencia(sec_a_analizar + ".fasta")  

    proteina = pasar_a_proteina(sec_fasta)
    #nombreProteina = blast_proteina_namePdb(proteina, sec_a_analizar)
    #nombrePdbInc = nombreProteina[:- 2]
    #buscaryGuardarPdb(nombrePdbInc)
    #nombrePdbProteina =  ("pdb"+nombrePdbInc+".ent").lower()

    if(validar_fasta(sec_fasta)):
        mut_letra = input("Desea hacer una mutacion manual 'M' o una automatica 'A': ").upper()
        posicion = int(input("Ingrese la posición donde quiere que comienze el análisis de la secuencia: ")) 

        if(posicion < len(sec_fasta)):
            prot_comienzo = sec_fasta[posicion-1:len(sec_fasta)]
        else:
            return print("Ingresó una posición fuera de rango, ingrese un número menor a: " + str(len(sec_fasta))) 

        mutacion = mutar_secuencia(prot_comienzo, mut_letra)
        #guardarEnFastaSeqMutada(mutacion)
        
        # graficar mutada
        #grafica proteina original
        pymol.finish_launching()
        __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
        #pymol.cmd.load('le/pdb3lee.ent')
        #pymol.cmd.load("le/"+nombrePdbProteina)


        # CR457033

        in_file = "mut.fasta"
        clustalw_cline = ClustalwCommandline("clustalw2", infile=in_file) # output='PIR'
        align = AlignIO.read("mut.aln", "clustal")
        clustalw_cline()
        print(align, "aCAAAAAAAAAAAAAAAA")
        print(clustalw_cline()," holaaaaa")
        
        '''                
        target='aln_pig_3v03'
        template='3V03_A'

        env = environ()
        aln = alignment(env)
        mdl = model(env, file="%s.pdb" % template, model_segment=('FIRST:A','LAST:A'))
        aln.append_model(mdl, align_codes=template, atom_files="%s.pdb" % template)
        aln.append(file='%s.ali'%target, align_codes=target)
        aln.align2d()
        aln.write(file='%s-%s.ali' % (target,template), alignment_format='PIR')
        aln.write(file='%s-%s.pap' % (target,template), alignment_format='PAP', alignment_features ="INDICES HELIX BETA")
        '''

        

        
        log.verbose()    # request verbose output
        env = environ()  # create a new MODELLER environment to build this model in
 
        # directories for input atom files
        env.io.atom_files_directory = './le/'
        env.io.hetatm = True
 
 
        a = automodel(env,
             alnfile  = 'aln_rat_3v03.pir', # alignment filename
             knowns   = ('3V03'),  #.pdp         # codes of the templates
             sequence = 'NM_134326') #mutacion              # code of the target
        a.starting_model= 1                 # index of the first model
        a.ending_model  = 1                 # index of the last model
                                   # (determines how many models to calculate)
        #a.make()         
        pymol.cmd.load('./le/3V03.pdb')  
        pymol.cmd.load('NM_134326.B99990001.pdb')
        print(a, "acaaaaaaaaa!!!!!!")
        
        #pymol.cmd.extra_fitname CA, 3V03, align, object=all_to_3V03_alignCA


        '''  
        e = environ()

        target= open('mut.aln')

        a = alignment(e, file= target, alignment_format='FASTA')
        a.write(file='%s.ali'%target, alignment_format='PIR')
        '''


        print("La proteina original: " + proteina)
        print("La proteina mutada:   " + pasar_a_proteina(mutacion))

    try:
        return mutacion
    except:
        return "Error"

programa()


######### Funciones que pueden servir ##########


def arn_codificante(peptido):
    cadena_nueva = []
    cadena_ARN = ""

    for letra in peptido:
        for k,v in diccionario_ARN.items():
            if(letra == k):
                cadena_nueva.append(v)
    return cadena_ARN.join(cadena_nueva)   

def polimerasa(secuencia):
    if(secuencia.count('​TATAAA')==0):  
        print("No posee la región de unión a la polimerasa")
    else:
        print("Posee la región de unión a la polimerasa")       

def formato_fasta(fasta):
    f = open (fasta,'r')
    mensaje = f.read()
    #f.close()
    return mensaje

def secuencias_iguales(sec):
    reverse_dict = {}
    for key, value in sec.items():
        try:reverse_dict[value].append(key)
        except:reverse_dict[value] = [key]
    return [value for key, value in reverse_dict.items() if len(value) > 1]

def mutacion_de_UUA_a_UAA(peptido):
    cadena_ARN = dividir_3(peptido)
    
    for n,letras in enumerate(cadena_ARN):
        if(letras == "UUA"):  
            cadena_ARN[n] = 'UAA'
    
    return cadena_ARN    

def porcentaje(secuencia, letra):
    longitud = len(secuencia)
    cant_l = secuencia.count(letra)

    return (cant_l) / longitud     