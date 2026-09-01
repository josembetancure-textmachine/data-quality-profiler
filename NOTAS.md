# Contexto

Este proyecto surgió como etapa inicial de mi camino de aprendizaje autónomo, el cual abarca Python, pandas, SQL, PyTorch y demás herramientas que me permitan dedicarme a NLP en un lapso de 2 años.

Ante el uso de la IA como generadora de código, estas notas pretenden, primero, ser una evidencia de mi proceso de pensamiento a medida que construía el código y, segundo, demostrar que interioricé los conceptos usados. Por supuesto, me apoyé en Claude como "instructor particular" para que me explicara qué debía usar, cómo y cuándo, mas no le asigné el rol de programador activo mediante _prompting_ o _vibe coding_. Todo lo construido en este proyecto fue hecho por mí.

**Esta es la primera iteración del código. Si es necesario más adelante, se introducirán en cada sección las versiones actualizadas y se indicará el motivo del cambio, bajo el subtítulo "Iteraciones".**

# if __name__=="__main__"

En esta primera parte defino las líneas necesarias para validar que la ejecución del _script_ mediante CLI funcione con normalidad.

```python
if __name__=="__main__":                                                                                                                        #primera línea
    if len(sys.argv)<2:                                                                                                                         #segunda línea
        print("Falta almenos un argumento. Debe ejecutar la herramienta así:\npython3 data_profiler.py archivo_a_analizar(con su extensión)")   #tercera línea
        sys.exit()                                                                                                                              #cuarta línea
    else:                                                                                                                                       #quinta línea
        df=sys.argv[1]                                                                                                                          #sexta línea
```
**Explicación del código:**
1. La primera línea abre un condicional que se cumple solo si el _script_ se ejecuta a sí mismo. En contraposición, cuando es otro _script_ el que ejecuta un _import_ de data_profiler.py, lo que está anidado dentro de este bloque no llega a ejecutarse.
2. Condicional para asegurar el número de argumentos que deben pasarse a través del CLI para la correcta ejecución del código. ```sys.argv[0]``` siempre es el nombre del _script_ que se quiere ejecutar; ```sys.argv[1]``` debe contener la ruta del archivo que se desea analizar. Por eso, ```len(sys.argv)<2``` funciona como medida de seguridad para que siempre se pasen estos dos argumentos.
3. Si lo anterior falla, entonces se imprime un mensaje de error.
4. Y, además (es decir, como consecuencia de ese fallo), también se detiene la ejecución del _script_.
5. De lo contrario:
6. Se define df y se le asigna el valor del str ```sys.argv[1]```. Es útil para conservar la ubicación del archivo que se pase por consola.

# class DataProfiler:

```python
class DataProfiler:                                                                                                 #primera línea
    def __init__(self,df):                                                                                          #segunda línea

        if not isinstance(df,pd.DataFrame):                                                                         #tercera línea
            if Path(df).suffix==".csv":                                                                             #cuarta línea
                self.source=df                                                                                      #quinta línea
                df=pd.read_csv(df)                                                                                  #sexta línea
            elif Path(df).suffix==".xlsx":                                                                          #séptima línea
                self.source=df                                                                                      #octava línea
                df=pd.read_excel(df)                                                                                #novena línea
            else:                                                                                                   #décima línea
                raise ValueError("La ruta del archivo a analizar contiene un error o es un formato no admitido."
                 " Solo se admiten formatos .csv, .xlsx y DataFrames."
                )                                                                                                   #undécima línea
        else:                                                                                                       #duodécima línea
            self.source="DataFrame en memoria"                                                                      #décimotercera línea
            df=pd.DataFrame(df)                                                                                     #décimocuarta línea

        self.df=df                                                                                                  #décimoquinta línea
```
**Explicación del código:**

1. Definición de la clase.
2. Definición de los parámetros de la clase.

Son dos los archivos con los que trabajará este _script_: .csv, .xlsx, aunque la base del procesamiento son los DataFrames. A continuación, en lugar de explicar línea por línea, se explica el funcionamiento general del bloque if:

3. Se comprueba, en primer término, si el argumento pasado a la función NO es de tipo pd.DataFrame. Exactamente eso es lo que hace la tercera línea de código. De ahí, se desprenden dos caminos que funcionan igual:
    - Si el sufijo de df es .csv (cuarta línea), entonces ```df=pd.read_csv(df)``` (sexta línea).
    - Si el sufijo es .xlsx, entonces ```df=pd.read_excel(df)``` (novena línea).
En cualquier caso, se captura ```self.source=df```(quinta y octava líneas) antes de convertir a DataFrame. De esta manera, self.source conserva el str que contiene el argumento exacto que se le dio a la clase.

Cabe aclarar que si ninguno de los dos casos anteriores se cumple, es decir, que el argumento pasado no sea una ruta que termine en .csv o .xlsx, se detiene el constructor de la función con un mensaje de error (décima y undécima líneas).

4. Si el argumento pasado ya es un pd.DataFrame, entonces ```self.source="DataFrame en memoria"``` (décimotercera línea) y ```df=pd.DataFrame(df)```(décimo cuarta línea).

Capturar el str que contiene el argumento exacto que se le dio a la clase tiene sus implicaciones en __repr__ y generar_reporte().

## Términos importantes a considerar:

- **Parámetro:** el parámetro, por sí mismo, es simplemente un _placeholder_ atado a una función. Es decir, puede ser "llenado" con cualquier argumento que se le pase a la misma. Su existencia es independiente al argumento, no obstante, pues está definido para la función y existe dentro de ella.
- **Argumento:** por el contrario, el argumento no existe por sí mismo sino hasta que se llama. Puede pensarse en el argumento como una manifestación concreta del parámetro en un momento determinado. Diferentes argumentos pueden "llenar" un mismo parámetro cada vez que se llaman.
- **Atributo:** es un concepto muy ligado a las clases. No necesariamente tienen que ser la manifestación de un argumento que "llena" un parámetro de una clase, pues pueden ser valores fijos, no variables. Más bien, el concepto se refiere a cualquier dato de una instancia (es decir, la manifestación de una clase) al que puede accederse via self. Por ejemplo, ```self.df=df```viene de la transformación de un argumento, pero ```self.source="DataFrame en memoria"```es un dato fijo que no viene de ningún argumento y que, además, tampoco se definió como parámetro. 

# Método __repr__():

Es una práctica indispensable cuando se trabaja con clases. La idea es que este método devuelva un _output_ tipo str, pero que se lea como código que pueda recrear un objeto de Python. Es importante para hacer visible el objeto durante el _debugging_/desarollo cada vez que Python necesita imprimirlo. Sin __repr__, cuando trato de imprimir un objeto, obtengo un _output_ ilegible e inútil. Por el contrario, con __repr__ puedo definir qué mostrará esa impresión (datos útiles y legibles).

Es importante considerar que también existe __str__. Cuando hago ```print(objeto)```y no hay __str__ definido, Python usa automáticamente el método __repr__. Si hay __str__ definido, Python lo usa por defecto, a menos de que se use la sintaxis ```print([objeto])``` (pues siempre que se trate de listas, tuplas, diccionarios o cualquier contenedor se despliega __repr__) o ```repr(objeto)```. 

Dentro del __repr__ se debe poner información útil sobre el objeto, y se debe usar !r cuando la variable es str, lo que no es necesario cuando es int.

```python
    def __repr__(self):                                                                                         #primera línea
        return f"DataProfiler(fuente={self.source!r}, filas={len(self.df)}, columnas={len(self.df.columns)})"   #segunda línea
```
1. Se define el método __repr__.
2. Se construye lo que devuelve este método. En este caso, se desea visualizar las características destacables del argumento con el que se construyó la clase:
    - fuente, es decir, si la fuente fue un archivo .csv, .xlsx o un DataFrame. Nótese que se usa !r, pues lo que contiene ```self.source```es tipo str.
    - filas, es decir, cuántas filas tiene el DataFrame (para este punto, ya df se transformó a un DataFrame).
    - columnas, es decir, cuántas columnas tiene el DataFrame.

# Método reporte_nulos():

La idea es evaluar cuántos datos tipo NaN, NaT y None hay en el DataFrame.

```python
    def reporte_nulos(self):        #primera línea
        return self.df.isna().sum() #segunda línea
```
1. Se define el método reporte_nulos().
2. Sobre el atributo ```self.df```se usa la función ```.isna()```para determinar cuántos valores del DataFrame son NaN, NaT o None. Algunas precisiones importantes sobre ```.isna()```son:
    - Esta función opera sobre cada uno de los valores del DataFrame. Devuelve una dato tipo pd.DataFrame a modo de máscara booleana donde se marcan con True aquellos valores NaN, NaT o None, y con False aquellos que no lo son.
    - Funciona exactamente igual a ```.isnull()```, es decir, son la misma función. Incluso, la documentación oficial dice que esta última es un alias de la primera.
    - ```.sum()``` opera sobre la máscara booleana. Como True es igual a 1 y False es igual a 0, el resultado es un int que representa el número total de valores que son NaN, NaT o None. ```.sum()```puede recibir el parámetro axis, el cual modifica la dirección de conteo. Por defecto, su valor es igual a 0, lo que significa que cuenta por columnas, es decir, devuelve una sumatoria de los valores de cada columna; axis igual a 1, por el contrario, devuelve una sumatoria total de los valores por fila.

# Método resporte_duplicados():

Sirve para evaluar las filas duplicadas dentro del DataFrame.

```python
    def reporte_duplicados(self):           #primera línea
        return self.df.duplicated().sum()   #segunda línea
```
1. Se define el método reporte_duplicados().
2. Sobre el atributo ```self.df``` se usa la función ```.duplicated()``` para determinar cuántas filas exactamente iguales (es decir, con los mismos valores en las mismas columnas) hay. Esta función opera al nivel de la fila y lo que hace es comparar una por una, sin importar si son adyacentes o no, para determinar cuáles de ellas son duplicadas. Como la función devuelve un dato tipo Series a modo de máscara booleana, ```.sum()```devuelve el total de filas duplicadas con las siguientes consideraciones:
    - Suponiendo que la fila con índice 0 sea exactamente igual a la fila con índice 3, por ejemplo, ```.duplicated()``` marcará la fila con índice 3 como True. Parecería, entonces, que soy hay una fila duplicada cuando en realidad son dos, pero es el comportamiento por defecto de esta función cuando no tiene parámetros (marca como True la fila de índice 3 por ser la duplicada de la fila con índice 0 que, al ser la primera, no es duplicada de ninguna). El parámetro keep es el que determina este comportamiento. Por defecto, es igual a "first". Sin embargo, si es igual a False, marca todas las duplicadas (para el caso, marcaría como True tanto la fila de índice 0 como la fila de índice 3); es útil cuando necesito saber, por ejemplo, el índice de las filas duplicadas. keep también puede ser igual a "last", el cual invierte el comportamiento por defecto (es decir, marcaría la fila con índice 3 como False y la fila con índice 0 como True).
    - Tiene otros parámetros como subset, que sirve para hacer el conteo de duplicados pero restringido a los valores de las columnas indicadas. Por defecto, ```.duplicated()``` opera a nivel de todas las columnas.