# UNQ Modeller

Unq-Modeller es una aplicacion con interfaz gráfica, basada en librerias de python donde el usuario podrá:

  - Obtener la secuencia limpia de un archivo **.fasta**.
  - Ver la proteina obtenida de dicho archivo.
  - Realizar un mutación a elección de la secuencia obtenida.
  - Las mutaciones disponibles son:
        - Mutacion Automaica: Se elije al azar una posicion y una letra a mutar, solo se escoje donde se desea iniciar el flujo de mutacion.
        - Mutacion Manual: Se elije, letra de aminoacido a mutar, posicion donde se desea mutar dicha letra, y tambien donde se desea iniciar el flujo de mutación.
  - Modelar las proteinas obtenidas.

# *Requisitos:*

- Es necesario tener en cuenta, que para obtener el funcionamiento optimo de nuestra aplicacion, debemos tener todas las librerias y software en nuestro equipo. 
- Nuestra recomendacion principal, es utilizar Anaconda, es por ello que mostraremos los metodos de instalación, mediante comandos  conda.
- No obstante, se pueden utilizar otos metódos de instalación(ej. Pip)

#### Anaconda
- Instalacion:
   - [Enlace a descarga para Windows](https://repo.anaconda.com/archive/Anaconda3-2019.10-Windows-x86_64.exe) 
   - [Enlace a descarga para Linux](https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh) 
- Los enlaces son para python 3.7 que es el requerido para nuestra aplicacion.

#### Pymol
- Instalacion por link:
   - [Enlace a descarga para Windows](https://pymol.org/installers/PyMOL-2.3.3_0-Windows-x86_64.exe) 
   - [Enlace a descarga para Linux](https://pymol.org/installers/PyMOL-2.3.4_121-Linux-x86_64-py37.tar.bz2)

- Instalacion conda:
    ```
    $ conda install -c schrodinger pymol
    ```  
    
#### Modeller 
- Instalacion por link:
   - [Enlace a descarga para Windows](https://salilab.org/modeller/9.23/modeller9.23-64bit.exe) 
   - [Enlace a descarga para Linux](https://salilab.org/modeller/9.23/modeller-9.23-1.x86_64.rpm)

- Instalacion conda:

    ```
    $ conda config --add channels salilab
    $ conda install modeller
    ``` 
    
#### BioPython
- Instalacion conda:
    ~~~
    $ conda install -c anaconda biopython
    ~~~ 
 
### lxml
- Instalacion conda:
    ```sh
    $ conda install -c anaconda lxml
    ```  

# *Informacion Biologica:*

En UNQ - Modeller se podran elegir parametros con los que la aplicacion funcionará, como el tipo de mutación, inicio, letra a mutar, posicion de letra a mutar, cantidad de modelos comparativos, etc.

Pero algunos otros paramtros utilizados en nuestra aplicación, ya vienen definidos por default, y el flujo de uso de la misma no permite elección, por este motivo a continuacion se detallarán sus parametros por default:

- **Búsqueda de Blast (NCBIWWW.qblast)**
    ```sh
    url_base='https://blast.ncbi.nlm.nih.gov/Blast.cgi',
    auto_format=None,
    composition_based_statistics=None,
    db_genetic_code=None,
    endpoints=None,
    entrez_query='(none)',
    expect=10.0, filter=None,
    gapcosts=None,
    genetic_code=None,
    hitlist_size=50,
    i_thresh=None,
    layout=None,
    lcase_mask=None,
    matrix_name=None,
    nucl_penalty=None,
    nucl_reward=None,
    other_advanced=None,
    perc_ident=None,
    phi_pattern=None,
    query_file=None,
    query_believe_defline=None,
    query_from=None,
    query_to=None,
    searchsp_eff=None,
    service=None,
    threshold=None,
    ungapped_alignment=None,
    word_size=None,
    short_query=None,
    alignments=500,
    alignment_view=None,
    descriptions=500,
    entrez_links_new_window=None,
    expect_low=None,
    expect_high=None,
    format_entrez_query=None,
    format_object=None,
    format_type='XML',
    ncbi_gi=None,
    results_file=None,
    show_overview=None,
    megablast=None,
    template_type=None,
    template_length=None
    ```  

- **Busqueda y descarga de PDB (retrieve_pdb_file)**
    ```sh
    obsolete=False,
    pdir=None,
    file_format=None,
    overwrite=False
    ```  

- **Busqueda de clustal (ClustalOmegaCommandline)**
   ```sh
   verbose=False,
   auto=True,
   force=True
   ```
   
- **Modelado**
   ```sh
   deviation=None,
   library_schedule=None,
   csrfile=None, inifile=None,
   assess_methods= asses.DOPE 
   ```

- **Visualizacion de proteinas**
   ```sh
    Se abriran en pymol no alineadas.
   ```
 
# *Flujo de uso:*

- **Preparación:**
    > 1- Clonar repositorio.

    > 2- Descargar archivo fasta de [Protein Data Bank](https://www.rcsb.org/).
    
    > 3- Colocar *.fasta* en carpeta SRC del repo clonado.
    
- **Uso correcto:**
    > 1- Colorcar nombre de archivo fasta.
    > 2- Clickear boton cargar para manipular datos.
    > 3- En caso de ser una secuencia valida y querer visuazlizar la secuencia cargada, o la proteina obtenida, seleccionar los botones respectivos.
    > 4- Clickear en continuar.
    > 5- Elegir tipo de mutacion requerida seleccionando el respectivo boton.
    > 6- Cargar los datos necesarios en los input segun eleccion de mutacion.
    > 7- Cargar datos para manipulacion.
    > 8- En caso de ser una mutacion exitosa, y querer visualizar la secuencia o proteina resultante, clickear en los respectivos botones.
    > 9- En caso de querer ver los datos manipulados hasta el momento, clickear el boton correspondiente.
    > 10- Ingresar la cantidad de modelos que desea comparar para luego obtener el mejor de ellos, recuerde, cuanto mas modelos mas tiempo de ejecucion, pero mejor indice de resultado.
    > 11- En el software de pymol que se ejectura, se podran colocar comandos de cealing,align o super.

- **Errores:**
    > Archivo inexistente: sucede en caso de haber cargado el nombre del archivo fasta vacio, o con un nombre incorrecto.

    > No hay archivo cargado: sucede en caso de querer continuar sin haber cargado un archivo fasta.
    
    > El archivo fasta es incorrecto, hay un stop dentro de la secuencia : sucede en caso de que haya un stop dentro del fasta ingresado por lo cual no se valido el analisis.
    
    > El archivo fasta es una proteina, ingrese una secuencia de ADN o ARN: sucede en caso de haber cargado un fasta de una proteina.
    
    > El tamaño de la secuencia no es el correcto: sucede en caso de ser demasiado pequeña la secuencia obtenida del fasta.
    
    > Debe elegir un tipo de mutacion y cargar los campos: sucede en caso de no haber elegido un tipo de mutacion o al dejar los campos de inputs sin valores.
    


   
  
