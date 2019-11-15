sec1 = 'AGEKGKKIFVQKCSQCHTVCSQCHTVEKGGKHKTGPNEKGKKIFVQKCSQCHTVLHGLFGRKTGQA'
 
diccionario_ARN = {
    "A":"GCU", "R":"AGA", "N":"AAU", "D":"GAU", "C":"UGC", "F":"UUU", "G":"GGC", 
    "E":"GAA", "Q":"CAG", "H":"CAU", "I":"AUU", "L":"UUA", "K":"AAA", "P":"CCU", 
    "S":"UCU", "Y":"UAU", "T":"ACU", "W":"UGG", "V":"GUA", "M":"AUG", "X":"UAA"  
}

def arn_codificante(peptido):
    cadena_nueva = []
    cadena_ARN = ""

    for letra in peptido:
        for k,v in diccionario_ARN.items():
            if(letra == k):
                cadena_nueva.append(v)
    return cadena_ARN.join(cadena_nueva)   

#print(arn_codificante(sec1))           

sec2 = 'GTTATAATATTGCTAAAATTATTCAGAGTAATATTGTGGATTAAAGCCACAATAAGATTTATAATCTTAAATGATGGGACTACCATCCTTACTCTCTCCATTTCAAGGCTGACGATAAGGAGACCTGCTTTGCCGAGGAGGTACTACAGTTCTCTTCACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTTTTAATATGTCCAGTATTCATTTTTGCATGTTTGGTTAGGCTAGGGCTTAGGGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTAGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTCTATTGTGCCATACTGTTGAATGTTTATAATGCATGTTCTGTTTCCAAATTTCATGAAATCAAAACATTAATTTATTTAAACATTTACTTGAAATGTTCACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTTTTAATATGTCCAGTATTCATTTTTGCATGTTTGGTTAGGCTAGGGCTTAGGGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTAGATTTATATATCAAAGGAGGCT'
sec3 = 'ACTTTGTTTTTATCTCCTGCTCTATTGTGCCATACTGTTGAATGTTTATACCCTACATGGTGCATGTTCTGTTTCCAAATTTCATGAAATCAAAACATTAATTTATTTAAACATTTACTTGAAATGTTCACAAACAATTGTCTTACAAAATGAATAAAACAGCACTTTGTTTTTATCTCCTGCTTTTAATATGTCCAGTATTCATTTTTGCATGTTTGGTTAGGCTAGGGCTTAGGGATTTATATATCAAAGGAGGCTTTGTACATGTGGGACAGGGATCTTATTTTAGATTTATATATCAAAGGAGGCT'

def polimerasa(secuencia):
    if(secuencia.count('​TATAAA')==0):  
        print("No posee la región de unión a la polimerasa")
    else:
        print("Posee la región de unión a la polimerasa")        


sec4 = 'AAUCAUGUAGUAGGCUUUUUUUUAGAUCAUGCU'
sec5 = 'GCUUAUCCUGCUUUGGCUCUGGCGUAUUAACUGGC'
sec6 = 'GCUUUAUAUCCUGCUUUGGCUCUGGCGUAUUAACU'

def dividir_3(cadena):
    lista_nueva = []
    for i in range(0, len(cadena), 3):
        lista_nueva.append(cadena[i:i+3])

    return lista_nueva


def mutacion(peptido):
    cadena_ARN = dividir_3(peptido)
    
    for n,letras in enumerate(cadena_ARN):
        if(letras == "UUA"):  
            cadena_ARN[n] = 'UAA'
    
    return cadena_ARN   

#print(dividir_3(prueba))
#print(mutacion(prueba))

def longitud(peptido):
    cadena_mutada = mutacion(peptido)
    longitud = 0

    for i in cadena_mutada:
        if i=='UAA':
            longitud = cadena_mutada.index(i) + 1

    return cadena_mutada[0:longitud]

#print(longitud(sec2))


secuencias = {
    'CitC_humano':'AGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA',
    'CitC_gorila':'AGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA',
    'CitC_pollo' :'AGDIEKGKKIFVQKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQA'
}

def secuencias_iguales(sec):
    reverse_dict = {}
    for key, value in sec.items():
        try:reverse_dict[value].append(key)
        except:reverse_dict[value] = [key]
    return [value for key, value in reverse_dict.items() if len(value) > 1]


sec7 = 'AGDVEKGKKIFIMK' #Proteina
sec8 = 'ATTGGACGTAATGC' #ADN
sec9 = 'AGGUACCGAUCCA'  #ARN
sec10 = 'ACUT'  #proteina
sec11 = 'ACT'

# ADN = A, C, G, T
# ARN = A, C, G. U

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
        print("La secuencia " + lista + ": es una proteina")  
    elif(es_adn(secuencia)):
        print("La secuencia " + lista + ": es un ADN")  
    elif(es_arn(secuencia)):
        print("La secuencia " + lista + ": es un ARN")  
    else:
        print("La secuencia " + lista + ": es una proteina")          


def formato_fasta(fasta):
    f = open (fasta,'r')
    mensaje = f.read()
    #f.close()
    return mensaje

def obtener_secuencia(fasta):
    sec_fasta = open(fasta)          
    lista = []
    cadena_final = ""

    for line in sec_fasta:
        if line[0] != '>':
            lista.append(line.strip())
        
    sec_fasta.close()
    
    return cadena_final.join(lista)

#print(obtener_secuencia('c_homo_sapiens.fasta'))    

def porcentaje(secuencia, letra):
    longitud = len(secuencia)
    cant_l = secuencia.count(letra)

    return (cant_l) / longitud    

def arn(secuencia):
    cadena = dividir_3(secuencia)
    cadena_nueva = []
    cadena_ARN = ""
 
    for letras in cadena:
        for k,v in diccionario_ARN.items():
            if(v.count(letras)):  
                cadena_nueva.append(k)

    return cadena_ARN.join(cadena_nueva)                      

def pasar_a_lista(cadena): 
    lista = []
    for char in cadena:
        lista.append(char)

    return lista 

def mutar_manual(peptido, index, letra):
    cadena_ADN = pasar_a_lista(peptido)
    cadena_Mutada = ""

    for n in (cadena_ADN):
        if(cadena_ADN.index(n) == index):  
            cadena_ADN[index] = letra

    return (cadena_Mutada.join(cadena_ADN))

print(mutar_manual(sec4,2,'x'))

def mutar_automatica(sec_fasta): # FALTAAAAAA HACER
    return "Mutacion automaticaaaaaa"

def mutar_secuencia(sec, mut_letra):
    if(mut_letra == 'M'):
        letra = input("Ingrese la letra del aminoácido que quiere mutar: ").upper()
        index = input("Ingrese la posición: ")
        return mutar_manual(sec, index, letra)
        
    elif(mut_letra == 'A'):
        return mutar_automatica(sec) 

    else: 
        return "La letra que eligió no es la correcta, debe elegir 'M' o 'A'"
    

def programa():
    sec_a_analizar = input("Ingrese la secuenencia que desea analizar: ")
    #letra = input("Sobre qué aminoácido quiere calcular el porcentaje: ").upper()
    sec_fasta = obtener_secuencia(sec_a_analizar + ".fasta")  
    #validar_secuencia(sec_fasta) #validar si es una secuencia correcta, si es ADN, ARN, Proteina

    mut_letra = input("Desea hacer una mutacion manual 'M' o una automatica 'A': ").upper()
    mutacion = mutar_secuencia(sec_fasta, mut_letra) # mutar automatica o manual

    #longitud = len(sec_fasta)
    #promedio = porcentaje(sec_fasta, letra)
    #print("Longitud de secuencia: " + str(longitud) + ", Porcentaje del aminoácido " + letra + ": " + str(promedio))

    print("Secuencia original: " + sec_fasta)
    print("Secuencia mutada:   " + mutacion)
    
    #return mutacion
    
print(programa())