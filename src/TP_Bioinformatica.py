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
from Bio.Align.Applications import ClustalOmegaCommandline
from Bio.Align.Applications import MSAProbsCommandline
from Bio.PDB.Entity import Entity 
from Bio.PDB import *

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

partChain = None
posicionMutada = 0
letraMutada = ""

def getPosicionMutada():
    global posicionMutada
    return posicionMutada     

def getLetraMutada():
    global letraMutada
    return letraMutada 

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
            return cadena_corta.join(lista[:longitud+1])
    
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

def msjerror_secFasta_invalida(secuencia):
    sec = que_es(secuencia)

    if(hay_stop(secuencia)):
        return ("El archivo fasta es incorrecto, hay un stop dentro de la secuencia")
    elif(sec=="proteina"):
        return ("El archivo fasta es una proteina, ingrese una secuencia de ADN o ARN")
    elif(len(secuencia)%3 !=0):
        return ("El tamaño de la secuencia no es el correcto")
    else:
        return ("Problema no identificado")

def validacion_mutacion(mutacionProteina, proteina):
    len_prot= len(proteina)
    len_mut = len(mutacionProteina)
    
    return ((len_mut/len_prot)*100) > 40
    
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
        return "El archivo no existe" 
    
def msjeError_archivoInexistente(fasta):
        try:
                sec_fasta = open(fasta)  
        except:
            return "No existe"

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
    global posicionMutada
    global letraMutada

    cadena_ADN = pasar_a_lista(sec_fasta)
    cadena_mutada = ""
    quees = que_es(sec_fasta)
    randPos = randint(0,(len(sec_fasta)-1))
    
    if(quees == "ADN"): 
        randLetra = random.choice("ACGT") 
        cadena_ADN.insert(randPos,randLetra)
        posicionMutada = int(randPos+1)
        letraMutada = str(randLetra)
        print("Mutó la letra: " + randLetra + " en la posición: " + str(randPos+1))
        
    elif(quees == "ARN"):
        randLetra = random.choice("ACGU") 
        cadena_ADN.insert(randPos,randLetra)
        posicionMutada = int(randPos+1)
        letraMutada = str(randLetra)
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
            index = int(input("Ingrese la posición donde quiere que mute el aminoácido: "))
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
    global partChain
    res = "La proteina no existe en la base de datos PDB"
    resultBlast = NCBIWWW.qblast(program= "blastp", database= "pdb", sequence= seq_proteina)
    blast = sec_a_analizar + ".xml"

    save_clk = open(blast, "w")
    save_clk.write(resultBlast.read())    
    save_clk.close()
    
    blast_records = NCBIXML.parse(open(blast))
    myScore = 0
    myPorcentaje = 0

    for blast_record in blast_records:
        for alignment in blast_record.alignments:
            porcentaje = alignment.hsps[0].identities / alignment.hsps[0].align_length
            if((porcentaje > myPorcentaje) and (alignment.hsps[0].expect <= 0.0)): # and (alignment.hsps[0].score > myScore)):
                myPorcentaje = porcentaje
                myScore = alignment.hsps[0].score
                res = alignment.accession
            elif(alignment.hsps[0].expect != 0.0):
                if((porcentaje > myPorcentaje) and (alignment.hsps[0].score > myScore)):
                    myPorcentaje = porcentaje
                    myScore = alignment.hsps[0].score
                    res = alignment.accession
    partChain = res[-1]   

    return res

class NotDisordered(Select):
    def accept_atom(self, atom):
        return not atom.is_disordered() or atom.get_altloc() == 'A'
    def accept_chain(self, chain):
        return chain.id == partChain

def buscaryGuardarPdb(nombrePdbInc): 
    pdbdownload = PDBList()
    pdbdownload.retrieve_pdb_file(nombrePdbInc, file_format="pdb")
    
    nombrePdbProteina = ('pdb'+nombrePdbInc).lower()
    carpeta = nombrePdbInc[1:-1]
    directorio = (carpeta+'/pdb'+nombrePdbInc+'.ent').lower()

    parser = PDBParser()
    s = parser.get_structure(nombrePdbProteina, directorio)
    io = PDBIO()

    io.set_structure(s)
    io.save(nombrePdbInc+'.pdb', select=NotDisordered())
    
def guardarEnFastaSeqMutadaYOriginal(proteina, mutacionProteina, nombrePdbInc):
    save_clk = open('prot_mut.fasta', 'w')
    save_clk.write('>mutacion'+'\n')
    save_clk.write(mutacionProteina + '\n')
    save_clk.write('>'+nombrePdbInc +'\n')    
    save_clk.write(proteina)
    save_clk.close()

def buscar_clustal():
    in_file = 'prot_mut.fasta'
        
    clustalomega_cline = ClustalOmegaCommandline(infile=in_file, outfmt="fasta", verbose=False, auto=True, force=True)
    clustalomega_cline()
        
    env = environ()
    target='prot_mut'
    a = alignment(env, file='%s.fasta'%target, alignment_format='FASTA')
    a.write(file='%s.ali'%target, alignment_format='PIR')

def generar_pir(nombrePdbInc):
    target='prot_mut'
    template= nombrePdbInc

    env = environ()
    aln = alignment(env)
    mdl = model(env, file="%s.pdb" % template, model_segment=('FIRST:A','LAST:A'))
    aln.append_model(mdl, align_codes=template, atom_files="%s.pdb" % template)
    aln.append(file='%s.ali'%target, align_codes='mutacion')
    aln.align2d()
    aln.write(file='%s_%s.ali' % (target,template), alignment_format='PIR')
    #aln.write(file='%s_%s.pap' % (target,template), alignment_format='PAP', alignment_features ="INDICES HELIX BETA")

def generar_modelado(nombrePdbInc, cant_modelos):
    log.verbose()    # request verbose output
    env = environ()  # create a new MODELLER environment to build this model in
 
    # directories for input atom files
    env.io.atom_files_directory = './:../atom_files'
    env.io.hetatm = True
 
    a = automodel(env,
            alnfile  = 'prot_mut_'+ nombrePdbInc +'.ali', # alignment filename
            knowns   = (nombrePdbInc),  #.pdp  # codes of the templates
            sequence = 'mutacion', #mutacion   # code of the target
            assess_methods=(assess.DOPE,
                            #soap_protein_od.Scorer(),
                            assess.GA341))
    a.starting_model= 1                 # index of the first model
    a.ending_model  = cant_modelos      # index of the last model
                                   # (determines how many models to calculate)
    a.md_level = refine.slow

    a.make() # Si se comenta rompe por el DOPE!!!!  

    # Get a list of all successfully built models from a.outputs
    ok_models = [x for x in a.outputs if x['failure'] is None]

    # Rank the models by DOPE score
    key = 'DOPE score'
    ok_models.sort(key=lambda a: a[key])

    # Get top model
    m = ok_models[0]
        
    print("Top model: %s (DOPE score %.3f)" % (m['name'], m[key]))
    pdb_mutacion = str(m['name'])

    return pdb_mutacion

def generar_pymol(nombrePdbInc, pdb_mutacion):
    pymol.finish_launching()
    __main__.pymol_argv = ['pymol','-qc'] # Pymol: quiet and no GUI
    pymol.cmd.load(nombrePdbInc + '.pdb') #'./le/'+ nombrePdbInc + '.pdb' 
    pymol.cmd.load(pdb_mutacion)

    #pymol.cmd.cealign, nombrePdbInc, pdb_mutacion, object='alineacion'
    #pymol.cmd.extra_fit, CA, nombrePdbInc, object='alineacion'
    #pymol.align(nombrePdbInc, pdb_mutacion, object='name')

"""
def programa():
    sec_a_analizar = input("Ingrese el nombre del archivo FASTA que desea analizar: ")
    sec_fasta = obtener_secuencia(sec_a_analizar + ".fasta")  

    if(validar_fasta(sec_fasta)):
        proteina = pasar_a_proteina(sec_fasta)

        #UTILIZACION DE BLAST
        nombreProteina = blast_proteina_namePdb(proteina, sec_a_analizar)
        nombrePdbInc = nombreProteina[:-2]
        global partChain
        partChain = nombreProteina[-1]
        buscaryGuardarPdb(nombrePdbInc)

        mut_letra = input("Desea hacer una mutacion manual 'M' o una automatica 'A': ").upper()
        posicion = int(input("Ingrese la posición donde quiere que comienze el análisis hasta el final de la secuencia: ")) 

        if(validar_fasta(sec_fasta[posicion-1:])):
            if(posicion < len(sec_fasta)):
                prot_comienzo = sec_fasta[posicion-1:len(sec_fasta)]
            else:
                return print("Ingresó una posición fuera de rango, ingrese un número menor a: " + str(len(sec_fasta))) 

            mutacion = mutar_secuencia(prot_comienzo, mut_letra)
            mutacionProteina = pasar_a_proteina(mutacion)
    
    
            if validacion_mutacion(mutacionProteina, proteina):
                guardarEnFastaSeqMutadaYOriginal(proteina, mutacionProteina, nombrePdbInc)
        
                buscar_clustal()
                generar_pir(nombrePdbInc)

                cant_modelos = int(input("Ingrese la cantidad de modelos a generar: ")) 
                pdb_mutacion = generar_modelado(nombrePdbInc, cant_modelos)
                generar_pymol(nombrePdbInc, pdb_mutacion)

                print("La proteina original: " + proteina)
                print("La proteina mutada:   " + pasar_a_proteina(mutacion))

            else:
                print("La secuencia mutada es demasiado pequeña para realizar un análisis")

    try:
        return mutacion
    except:
        return "Error"

    # CR457033 # 3LEE 
    # 6n5k # 4YO2
    # EU574314 5JRJ
    # 6SZS stop en el medio

    #cealign 3LEE, mutacion.B99990002, object=aln
    #cealign 4YO2, mutacion.B99990002, object=aln
    #cealign 5JRJ, mutacion.B99990002, object=aln

    # mutar Manual CR457033 aminoacido: T , posicion: 13

programa()
"""