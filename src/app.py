from TP_Bioinformatica import *
from tkinter import *
from tkinter import messagebox as MessageBox

### CREO UN STORE (para almacenar los datos del actual analisis)
class Datos:
    hayArchivoCargado = False   ## Denota true si se carga un archivo
    nombreArchivoCargado = ''   ## Indica el nombre del archivo cargado
    secuencia = ''              ## Secuencia original ingresada a partir de archivo fasta.
    proteina = ''               ## Proteina obtenida de la secuencia original.
    tipoMutacion = ''           ## Tipo de mutacion elegida.
    inicioDeMutacion = 0        ## Inicio donde quiere comenzar la mutacion.
    letraDeAmino = ''           ## En caso de mut manual, letra del aminoacido elejido.
    posicionDeMutAmino = 0      ## En caso de muta manual, posicion del aminoacido a mutar.
    secuenciaRecortada = ''     ## Secuencia recortada definida por el inicio de la mutacion.
    secuenciaMutada = ''        ## Secuencia resultante de la mutacion.
    proteinaMutada = ''         ## Proteina resultante de la mutacion.
    nombreProteina = ''         ## Nombre proteina original.
    nombrePdb = ''              ## Nombre del pdb de proteina original.      
    poscionDeMutAutomaticaAmino  = 0 

datos = Datos()

## CREACION DE VENTANA NUMERO 1. (INGRESAR SECUENCIA FASTA)

secuenciaActual = ""

ventanaIngresoFasta = Tk()                  ## Creacion panel general
ventanaIngresoFasta.title("UNQ - Modeller") ## Titulo 
ventanaIngresoFasta.geometry('350x250')     ## Tamaño

### Creacion de textlabel (1).
ingreseFastaTxt = Label(ventanaIngresoFasta,
 text="Ingrese el nombre del archivo FASTA que desea analizar:")        ## Texto
ingreseFastaTxt.place(x=10,y=5)                                         ## Posicion

### Creacion de Input (2) para nombre de secuncia.
nombreDeFasta = Entry(ventanaIngresoFasta,width=20)                     ## BoxInput 
nombreDeFasta.place(x=35,y=45)                                          ## Posicion

### Accion de boton ver secuencia(3).
def onHandlerVerSecuencia():
    msjeVerSecunecia = MessageBox.showinfo(message = datos.secuencia, title="Secuencia obtenida")
    return msjeVerSecunecia

### Creacion de boton ver secuencia (3).
verSecuencia = Button(ventanaIngresoFasta, 
text="Ver Secuencia",width=30, state='disabled', command= onHandlerVerSecuencia)
verSecuencia.place(x=50,y=85)


### Accion de boton ver proteina(4).
def onHandlerVerProteina():
    msjeVerProteina = MessageBox.showinfo(message = datos.proteina, title="Proteina obtenida")
    return msjeVerProteina


### Creacion de boton ver proteina(4). 
verProteina = Button(ventanaIngresoFasta, 
text="Ver Proteina",width=30, state='disabled', command = onHandlerVerProteina)
verProteina.place(x=50,y=125)    

### Accion boton cargar archivo (5).
def onHandleCargar():   
    datos.nombreArchivoCargado = nombreDeFasta.get() ## (obengo texto del textInput)
    datos.secuencia = obtener_secuencia(datos.nombreArchivoCargado + ".fasta") 
    mensaje_error = msjerror_secFasta_invalida(datos.secuencia)

    if(msjeError_archivoInexistente(datos.nombreArchivoCargado + ".fasta") != "No existe"):
        if validar_fasta(datos.secuencia):
            verSecuencia.configure(state="normal")
            verProteina.configure(state="normal")
            datos.hayArchivoCargado = True
            datos.proteina = pasar_a_proteina(datos.secuencia)                  
        else:
            alertaFastaIncorrecto = MessageBox.showinfo(message = mensaje_error,
             title="Error de Fasta")
    else:
        alertaFastaInexistente = MessageBox.showinfo(message = "Archivo inexistente",
         title="Error de Fasta")

### Creacion de boton cargar archivo(5).
cargarFasta = Button(ventanaIngresoFasta,
 text="Cargar",command= onHandleCargar ,width=15)
cargarFasta.place(x=200,y=42)       



### Accion boton Continuar
def crearVentanaDeMutacion():

    if(datos.hayArchivoCargado):
    
        ventanaDeMutacion = Tk()
        ventanaIngresoFasta.withdraw()
        ventanaDeMutacion.title("UNQ - Modeller - Mutacion")
        ventanaDeMutacion.geometry('500x500')

        ### Creacion de textlabel (1).
        eligaTipoMutTxt = Label(ventanaDeMutacion,
        text="Seleccione el tipo de mutacion que desea realizar:")
        eligaTipoMutTxt.place(x=10,y=5)
    
        ### Creacion de textLabel (2).  
        ingresePosicionTxt = Label(ventanaDeMutacion, 
        text="Ingrese la posición donde quiere que comience el análisis hasta el \n final de la secuencia:") 
        ingresePosicionTxt.place(x=10,y=90)   
        
        ### Creacion de input (3) para ingresar posicion de inicio de mut. 
        posicionDeMut = Entry(ventanaDeMutacion,width=10, state='disabled')
        posicionDeMut.place(x=400,y=105)

        ### Creacion de textLabel (4). 
        casoMutManualTxt = Label(ventanaDeMutacion, 
        text="En caso de haber elegido Mutacion manualcomplete los siguientes campos:") 
        casoMutManualTxt.place(x=10,y=150)  

        ### Creacion de textLabel (5).  
        ingreseLetraAminoTxt = Label(ventanaDeMutacion, 
        text="Ingrese la letra del aminoácido en el que va a mutar:") 
        ingreseLetraAminoTxt.place(x=10,y=180)   

        ### Creacion input (6) para ingresar letra de aminoacido mutManual.
        letraDeMut = Entry(ventanaDeMutacion,width=10, state='disabled')
        letraDeMut.place(x=400,y=180)

        ### Creacion de textLabel (7).  
        ingresePosAminoTxt = Label(ventanaDeMutacion, 
        text="Ingrese la posición donde quiere que mute el aminoácido:") 
        ingresePosAminoTxt.place(x=10,y=210)   

        ### Creacion input (8) para ingresar letra de aminoacido mutManual.
        posDeAmino = Entry(ventanaDeMutacion,width=10, state='disabled')
        posDeAmino.place(x=400,y=210)

        ##Creacion acciones botones mut manual y mut automatica (9)
        def onHandlerMutacionManual():
            datos.tipoMutacion = 'M'
            posicionDeMut.configure(state='normal')
            letraDeMut.configure(state='normal')
            posDeAmino.configure(state='normal')
        
        def onHandlerMutacionAutomatica():
            datos.tipoMutacion = 'A'
            posicionDeMut.configure(state='normal')
            letraDeMut.configure(state='disabled')
            posDeAmino.configure(state='disabled')

        ### Creacion de botones de mutacion Manual, mutacion autmatica (9).
        mutManual = Button(ventanaDeMutacion, text="Mutacion manual",width=30, command=onHandlerMutacionManual)
        mutManual.place(x=15,y=45)
        mutAutomatica = Button(ventanaDeMutacion, text="Mutacion automatica",width=30, command=onHandlerMutacionAutomatica)
        mutAutomatica.place(x=250,y=45)

        ### Creacion de accion ver secuencia mutada (11)    
        def onHandlerVerSecuenciaMutada():
            MessageBox.showinfo(title= 'Secuencia mutada', message= datos.secuenciaMutada)

        ### Creacion boton ver secuencia mutada (11)
        verSecMutada = Button(ventanaDeMutacion, 
        text="Ver secuencia mutada",width=30, state='disabled', command= onHandlerVerSecuenciaMutada)
        verSecMutada.place(x=120,y=290)

        ### Creacion de accion ver proteina mutada (12)    
        def onHandlerVerProteinaMutada():
            MessageBox.showinfo(title= 'Proteina mutada', message= datos.proteinaMutada)

        ### Creacion boton ver proteina mutada (12)
        verProtMutada = Button(ventanaDeMutacion, 
        text="Ver proteina mutada",width=30, state='disabled', command= onHandlerVerProteinaMutada)
        verProtMutada.place(x=120,y=330)

        ### Creacion labelText (13) para cant modelos.
        ingreseCantModelTxt = Label(ventanaDeMutacion, 
        text='Ingrese la cantidad de modelos a generar(mayor cantidad,mayor tiempo)')
        ingreseCantModelTxt.place(x=5,y=410)

        ### Creacion de input de cant de modelos (13).
        cantModelos = Entry(ventanaDeMutacion,width=10, state='disabled')
        cantModelos.place(x=400,y=410)

        ## Creacion de accion boton ver datos adicionales (13.5)
        def onHandlerVerDatos():
            MessageBox.showinfo(title='Datos obtenidos',
            message =
             "Nombre de archivo cargado" + datos.nombreArchivoCargado + "\n" +
             "Inicio de mutacion: " + str(datos.inicioDeMutacion) + "\n" + 
             "Tipo de mutacion: " + datos.tipoMutacion + "\n" +
             "Letra de aminoacido a mutar: " + datos.letraDeAmino + "\n"+ 
             "Posicion de aminoacido a mutar: " + str(datos.posicionDeMutAmino +1) + "\n" +
             "Nombre de pdb-proteina:" +  datos.nombrePdb)


        ### Creacion de boton ver datos adicionales(13.5)
        verDatosAdicionales = Button(ventanaDeMutacion, 
        text="Ver datos obtenidos", width=30, state='disabled', command= onHandlerVerDatos)
        verDatosAdicionales.place(x=120,y=370)

        ### Creacion de accion modelar (14)
        def onHandlerModlear():
            buscaryGuardarPdb(datos.nombrePdb)

            if validacion_mutacion(datos.proteinaMutada, datos.proteina):

                guardarEnFastaSeqMutadaYOriginal(datos.proteina, datos.proteinaMutada, datos.nombrePdb) 

                buscar_clustal()
                generar_pir(datos.nombrePdb)

                cant_modelos = int(cantModelos.get())
                pdb_mutacion = generar_modelado(datos.nombrePdb, cant_modelos)

                generar_pymol(datos.nombrePdb, pdb_mutacion)

            else:
                MessageBox.showinfo(title='Error', message='La secuencia mutada es demasiado pequeña para realizar un análisis')

        ### Creacion de boton modelar(14)
        modelar = Button(ventanaDeMutacion, 
        text="Modelar", width=30, state='disabled', command= onHandlerModlear)
        modelar.place(x=120,y=450)


        
        ### Accion de boton cargar(10).
        def onHandlerCargar():
            if(str(posicionDeMut.get())):
                datos.inicioDeMutacion = int(posicionDeMut.get())

                if(validar_fasta(datos.secuencia[datos.inicioDeMutacion-1:])):
                    if(datos.inicioDeMutacion < len(datos.secuencia)):
                        datos.secuenciaRecortada = datos.secuencia[datos.inicioDeMutacion-1:len(datos.secuencia)]
                        verProtMutada.configure(state='normal')
                        verSecMutada.configure(state='normal')
                        cantModelos.configure(state='normal')
                        modelar.configure(state='normal')
                        verDatosAdicionales.configure(state='normal')
                        datos.nombreProteina = blast_proteina_namePdb(datos.proteina, datos.nombreArchivoCargado)
                        datos.nombrePdb = datos.nombreProteina[:-2]
                        setPartChain(datos.nombreProteina[-1])
                        if(datos.nombreProteina != "La proteina no existe en la base de datos PDB"):
                            if(datos.tipoMutacion == 'A'):
                                datos.posicionDeMutAmino =  posicionMutada
                                datos.secuenciaMutada = mutar_automatica(datos.secuenciaRecortada)
                                MessageBox.showinfo(message="Mutacion extiosa",title="Mutacion")
                            else:
                                datos.posicionDeMutAmino =  int(posDeAmino.get())-1
                                datos.letraDeAmino = letraDeMut.get().upper()
                                datos.secuenciaMutada = mutar_manual(datos.secuenciaRecortada,datos.posicionDeMutAmino,datos.letraDeAmino)
                                MessageBox.showinfo(message="Mutacion extiosa",title="Mutacion")
                        else:
                            MessageBox.showinfo(message="La proteina no existe en la base de datos PDB", title= "Error")
                                
                    else:
                        verProtMutada.configure(state='disabled')
                        verSecMutada.configure(state='disabled')
                        MessageBox.showinfo(message="Ingresó una posicion fuera de rango",title="Error")
                else:
                    verProtMutada.configure(state='disabled')
                    verSecMutada.configure(state='disabled')
                    MessageBox.showinfo(message=msjerror_secFasta_invalida(datos.secuencia[datos.inicioDeMutacion-1:]),title="Error")

                datos.proteinaMutada = pasar_a_proteina(datos.secuenciaMutada)

            else:
                MessageBox.showinfo(message="Debe elegir un tipo de mutacion y completas los campos",title="Error")
        
        ### Creacion de boton cargar datos (10).
        cargarDatos = Button(ventanaDeMutacion, 
        text="Cargar datos",width=30, command= onHandlerCargar)
        cargarDatos.place(x=120,y=250)

    else:
         MessageBox.showinfo(message="No puede avanzar si cargar archivo fasta",title="Error")
         
## Creacion de Boton continuar(6).
continuar = Button(ventanaIngresoFasta, text="Continuar",width=17, state='normal', command = crearVentanaDeMutacion)
continuar.place(x=185,y=185)

## Creacion Accion boton salir(7).
def onHandlerSalir():
    ventanaIngresoFasta.withdraw()

## Creacion de Boton salir(7).
salir = Button(ventanaIngresoFasta, text="Salir",width=17, state='normal', command = onHandlerSalir)
salir.place(x=35,y=185)


    
    
ventanaIngresoFasta.mainloop()