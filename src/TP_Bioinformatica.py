import string
import random
from random import randint
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
sec5 = 'GCUUAUCCUGCUUUGGCUCUGGCGUAUUAACUGGC'
sec6 = 'GCUUUAUAUCCUGCUUUGGCUCUGGCGUAUUAACU'
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
 
# Falta arreglar diccionario
diccionario_ARN = {
    "A":"GCU", "R":"AGA", "N":"AAU", "D":"GAU", "C":"UGC", "F":"UUU", "G":"GGC", 
    "E":"GAA", "Q":"CAG", "H":"CAU", "I":"AUU", "L":"UUA", "K":"AAA", "P":"CCU", 
    "S":"UCU", "Y":"UAU", "T":"ACU", "W":"UGG", "V":"GUA", "M":"AUG", "X":"UAA"  
}

# ADN = A, C, G, T
# ARN = A, C, G. U

def dividir_3(cadena):
    lista_nueva = []
    for i in range(0, len(cadena), 3):
        lista_nueva.append(cadena[i:i+3])

    return lista_nueva   

def stop(cadena_mutada): # Corta la lista si encuentra un stop "UAA"
    longitud = 0
    for i in cadena_mutada:
        if i=='UAA':
            longitud = cadena_mutada.index(i) + 1

    return cadena_mutada[0:longitud]

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

def obtener_secuencia(fasta):
    sec_fasta = open(fasta)          
    lista = []
    cadena_final = ""

    for line in sec_fasta:
        if line[0] != '>':
            lista.append(line.strip())
        
    sec_fasta.close()
    return cadena_final.join(lista)                         

def pasar_a_lista(cadena): 
    lista = []
    for char in cadena:
        lista.append(char)

    return lista 

def mutar_manual(peptido, index, letra):
    cadena_ADN = pasar_a_lista(peptido)
    cadena_Mutada = ""

    cadena_ADN.insert(index,letra)
    del cadena_ADN[index+1]
   
    return (cadena_Mutada.join(cadena_ADN))

def mutar_automatica(sec_fasta): 
    cadena_ADN = pasar_a_lista(sec_fasta)
    cadena_Mutada = ""
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
    return (cadena_Mutada.join(cadena_ADN))

def mutar_secuencia(sec, mut_letra):
    if(mut_letra == 'M'):
        letra = input("Ingrese la letra del aminoácido en el que va a mutar: ").upper()
        index = int(input("Ingrese la posición: "))
        if(index > len(sec)):
            return "Ingresó una posición fuera de rango, ingrese un número menor a: " + str(len(sec))
        else:    
            return mutar_manual(sec, (index-1), letra)
        
    elif(mut_letra == 'A'):
        return mutar_automatica(sec) 

    else: 
        return "La letra que eligió no es la correcta, debe elegir 'M' o 'A'"
    

def programa():
    sec_a_analizar = input("Ingrese la secuenencia que desea analizar: ")
    sec_fasta = obtener_secuencia(sec_a_analizar + ".fasta")  
    #validar_secuencia(sec_fasta) #validar si es una secuencia correcta, si es ADN, ARN, Proteina

    mut_letra = input("Desea hacer una mutacion manual 'M' o una automatica 'A': ").upper()
    mutacion = mutar_secuencia(sec_fasta, mut_letra) # mutar automatica o manual

    print("Secuencia original: " + sec_fasta)
    print("Secuencia mutada:   " + mutacion)
    
    #return mutacion
    
print(programa())



######### Funciones que pueden servir ##########


def arn_codificante(peptido):
    cadena_nueva = []
    cadena_ARN = ""

    for letra in peptido:
        for k,v in diccionario_ARN.items():
            if(letra == k):
                cadena_nueva.append(v)
    return cadena_ARN.join(cadena_nueva)   

def arn(secuencia):
    cadena = dividir_3(secuencia)
    cadena_nueva = []
    cadena_ARN = ""
 
    for letras in cadena:
        for k,v in diccionario_ARN.items():
            if(v.count(letras)):  
                cadena_nueva.append(k)

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