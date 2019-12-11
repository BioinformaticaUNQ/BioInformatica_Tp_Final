from TP_Bioinformatica import *
from tkinter import *
from tkinter import messagebox as MessageBox

### CREO UN STORE (para almacenar los datos del actual analisis)
class Datos:
    secuencia = ''
    proteina = ''
    tipoMutacion = ''
    inicioDeMutacion = 1
    letraDeAmino = ''
    posicionDeMutAmino = 1

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
    nombre_archivo_fasta = nombreDeFasta.get() ## (obengo texto del textInput)
    sec_fasta = obtener_secuencia(nombre_archivo_fasta + ".fasta") 
    mensaje_error = msjerror_secFasta_invalida(sec_fasta)

    if(msjeError_archivoInexistente(nombre_archivo_fasta + ".fasta") != "No existe"):
        if validar_fasta(sec_fasta):
            verSecuencia.configure(state="normal")
            verProteina.configure(state="normal")
            datos.secuencia = sec_fasta
            datos.proteina = pasar_a_proteina(sec_fasta)                  
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




def crearVentanaDeMutacion():

    ventanaDeMutacion = Tk()
    ventanaDeMutacion.title("UNQ - Modeller - Mutacion")
    ventanaDeMutacion.geometry('500x500')

    ### Creacion de textlabel (1).
    eligaTipoMutTxt = Label(ventanaDeMutacion,
     text="Seleccione el tipo de mutacion que desea realizar:")
    eligaTipoMutTxt.place(x=10,y=5)
 
    ### Creacion de textLabel (2).  
    ingresePosicionTxt = Label(ventanaDeMutacion, 
    text="Ingrese la posición donde quiere que comienze el análisis:") 
    ingresePosicionTxt.place(x=10,y=90)   
      
    ### Creacion de input (3) para ingresar posicion de inicio de mut. 
    posicionDeMut = Entry(ventanaDeMutacion,width=10, state='disabled')
    posicionDeMut.place(x=400,y=90)

    ### Creacion de textLabel (4). 
    casoMutManualTxt = Label(ventanaDeMutacion, 
    text="En caso de haber elegido Mutacion manualcomplete los siguientes campos:") 
    casoMutManualTxt.place(x=10,y=120)  

    ### Creacion de textLabel (5).  
    ingreseLetraAminoTxt = Label(ventanaDeMutacion, 
    text="Ingrese la letra del aminoácido en el que va a mutar:") 
    ingreseLetraAminoTxt.place(x=10,y=150)   

    ### Creacion input (6) para ingresar letra de aminoacido mutManual.
    letraDeMut = Entry(ventanaDeMutacion,width=10, state='disabled')
    letraDeMut.place(x=400,y=150)

    ### Creacion de textLabel (7).  
    ingresePosAminoTxt = Label(ventanaDeMutacion, 
    text="Ingrese la posición donde quiere que mute el aminoácido:") 
    ingresePosAminoTxt.place(x=10,y=180)   

    ### Creacion input (8) para ingresar letra de aminoacido mutManual.
    posDeAmino = Entry(ventanaDeMutacion,width=10, state='disabled')
    posDeAmino.place(x=400,y=180)

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
    
    ### Accion de boton cargar(10).
    def onHandlerCargar():
        if(datos.tipoMutacion == 'A'):
            datos.inicioDeMutacion = int(posicionDeMut.get())
            MessageBox.showinfo(message = "Carga exitos", title="Carga de datos")
        else:
            datos.inicioDeMutacion = int(posicionDeMut.get())
            datos.letraDeAmino = letraDeMut.get()
            datos.posicionDeMutAmino = int(posDeAmino.get())
            MessageBox.showinfo(message = "Carga exitos", title="Carga de datos")

    


        

    ### Creacion de boton ver secuencia (10).
    verSecuencia = Button(ventanaDeMutacion, 
    text="Cargar datos",width=30, command= onHandlerCargar)
    verSecuencia.place(x=250,y=220)





              
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