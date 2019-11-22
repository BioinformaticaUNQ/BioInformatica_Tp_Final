from Model import *
from tkinter import *

secuenciaActual = ""

window = Tk()
 
window.title("UNQ - Modeller")
 
window.geometry('350x200')

## Text
 
ingreseFastaTxt = Label(window, text="Ingrese el nombre del archivo FASTA que desea analizar:")
 
ingreseFastaTxt.place(x=10,y=5)

## Text Input 

nombreDeFasta = Entry(window,width=20)

nombreDeFasta.place(x=35,y=45)


## Secuencia obtenida solo texto

secuencia = Label(window, text="Secuencia obtenida:", foreground="blue")
 
secuencia.place(x=10,y=85)


## Secuencia Obtenida Text

secuenciaObtenida = Label(window, text="No ha ingresado una secuencia aún", foreground="blue")

secuenciaObtenida.place(x=130,y=85)

def setSecuenciaActual(secuencia):
    secuenciaActual = secuencia


def clickearBotonCargar():
    
    sec_a_analizar = nombreDeFasta.get()
    
    sec_fasta = obtener_secuencia(sec_a_analizar + ".fasta") 
    
    proteinaActual = pasar_a_proteina(sec_fasta)
    
    if (proteinaActual == ""):
        secuenciaObtenida.configure(text="Ingrese nombre correcto")
    else:
        secuenciaObtenida.configure(text=sec_fasta)
        setSecuenciaActual(sec_fasta)
        

        
#### Boton cargar.

cargarFasta = Button(window, text="Cargar",command=clickearBotonCargar,width=15)

cargarFasta.place(x=200,y=42)         


## Boton Continuar

continuarButton = Button(window, text="Continuar",width=20)

continuarButton.place(x=15,y=150)

def reiniciar():
    secuenciaObtenida.configure(text="No ha ingresado una secuencia aún")

## Boton Borrar

cerrarButton = Button(window, text="Reiniciar",command=reiniciar(),width=20)

cerrarButton.place(x=170,y=150)



################################ VENTANA DE MUTACION ################################


ventanaDeMutacion = Tk()

ventanaDeMutacion.title("UNQ - Modeller - Mutacion")
 
ventanaDeMutacion.geometry('350x200')

## Text
 
eligaTipoDeMutacion = Label(ventanaDeMutacion,
                            text="Seleccione el tipo de mutacion que desea realizar:")
 
eligaTipoDeMutacion.place(x=10,y=5)

## Opciones

selected = IntVar()

rdBManual = Radiobutton(ventanaDeMutacion,text="Manual",value=1,
                        variable=selected).place(x=40,y=30)

rdBAutomatico = Radiobutton(ventanaDeMutacion,text="Automatico",value=2,
                            variable=selected).place(x=40,y=55)


def mut_letra():
    if (selected == 1):
        return "M"
    else:
        return "A"
    
 ## EligaPosicionTxt

EligaPosicionTxt = Label(ventanaDeMutacion, text="Elija posicion de inicio:")
 
EligaPosicionTxt.place(x=10,y=90)   
  
## Text Input 

posicionDeMut = Entry(ventanaDeMutacion,width=10)

posicionDeMut.place(x=170,y=90)


def posicion():
    return (int(posicionDeMut.get()))

def s():
    if(validar_fasta(secuenciaActual)):
    
        if(posicion() < len(secuenciaActual)):
            prot_comienzo = secuenciaActual[posicion()-1:len(secuenciaActual)]
        else:
            return print("Ingresó una posición fuera de rango, ingrese un número menor a: " + str(len(sec_fasta))) 

        mutacion = mutar_secuencia(prot_comienzo, mut_letra())

        # pasar_a_proteina(mutacion) ?????????
        # graficar

        print("La proteina original: " + proteina)
        print("La proteina mutada:   " + pasar_a_proteina(mutacion))

    try:
        return mutacion
    except:
        return "Error"

    
    
window.mainloop()