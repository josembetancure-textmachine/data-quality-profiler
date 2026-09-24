# Contexto

Este proyecto surgió como etapa inicial de mi camino de aprendizaje autónomo, el cual abarca Python, pandas, SQL, PyTorch y demás herramientas que me permitan dedicarme a NLP en un lapso de 2 años.

Ante el uso de la IA como generadora de código, estas notas pretenden, primero, ser una evidencia de mi proceso de pensamiento a medida que construía el código y, segundo, demostrar que interioricé los conceptos usados. Por supuesto, me apoyé en Claude como "instructor particular" para que me explicara qué debía usar, cómo y cuándo, mas no le asigné el rol de programador activo mediante _prompting_ o _vibe coding_. Todo lo construido en este proyecto fue hecho por mí.

**De ser necesario, cada sección contendrá un apartado para explicar los intentos fallidos de código con el objetivo de consolidar mejor el aprendizaje.**

# if __name__=="__main__"

En esta primera parte se definen las líneas necesarias para validar que la ejecución del _script_ mediante CLI funcione con normalidad.

```python
if __name__=="__main__":                                                                                                                        #primera línea
    if len(sys.argv)<2:                                                                                                                         #segunda línea
        print("Falta almenos un argumento. Debe ejecutar la herramienta así:\npython3 data_profiler.py archivo_a_analizar(con su extensión)")   #tercera línea
        sys.exit()                                                                                                                              #cuarta línea
    else:                                                                                                                                       #quinta línea
        df=sys.argv[1]                                                                                                                          #sexta línea
```
## **Explicación del código:**
1. La primera línea abre un condicional que se cumple solo si el _script_ se ejecuta a sí mismo. En contraposición, cuando es otro _script_ el que ejecuta un _import_ de data_profiler.py, lo que está anidado dentro de este bloque no llega a ejecutarse.
2. Condicional para asegurar el número de argumentos que deben pasarse a través del CLI para la correcta ejecución del código. ```sys.argv[0]``` siempre es el nombre del _script_ que se quiere ejecutar; ```sys.argv[1]``` debe contener la ruta del archivo que se desea analizar. Por eso, ```len(sys.argv)<2``` funciona como medida de seguridad para que siempre se pasen estos dos argumentos.
3. Si lo anterior falla, entonces se imprime un mensaje de error.
4. Y, además (es decir, como consecuencia de ese fallo), también se detiene la ejecución del _script_.
5. De lo contrario:
6. Se define df y se le asigna el valor del str ```sys.argv[1]```. Es útil para conservar la ubicación del archivo que se pase por consola.

**Iteración después de construir generar_reporte():**
```python
        with open("ejemplo_reporte.md","w") as ejemplo:
            contenido_informe = DataProfiler(df).generar_reporte()
            ejemplo.write(contenido_informe)
```
Se escribe dentro de de este bloque porque genera un _output_ a partir del script data_profiler.py. Dentro de este bloque, se evita que se genere el reporte en caso de que simplemente se quieran importar sus métodos desde otro archivo, en cuyo caso __name__ == "archivo que importa", diferente a "__main__", el nombre como tal de data_profiler.py

1. La función ```.open()``` sirve para crear o escribir archivos de acuerdo con los argumentos que reciba: (ruta, modo). 
    - El primero de ellos contiene la ruta del archivo que se quiera crear. Por defecto, el script resuelve la ruta desde la que está parada la terminal, no desde la cual vive el código. Si se quisiera crear un archivo en la ruta en la que vive el código, se debe usar ```Path(__file__).resolve().parent```, pues incluso ```Path.cwd()``` resuelve para la ruta de la terminal. El comportamiento deseado, en este caso, es este último (es decir, ```Path.cwd()```), pues lo más probable es que el usuario ejecute el script desde donde vive el archivo que quiere analizar y, por tanto, sería la ruta lógica para guardar el reporte.
    - Modo: son 4
        - "r", de solo lectura, es el modo por defecto cuando no se explícita. Lee un archivo existente (es decir, si el archivo no existe, el código falla).
        - "w", de escritura. Crea el archivo si este no existe, pero lo sobreescribe por completo.
        - "a", de escritura. No sobreescribe el archivo por completo, sino que agrega al final del mismo.
        - "x", de creación exclusiva. Si el archivo ya existe, el código falla.
Para este caso, se usa "w", pues se garantiza la creación de un archivo si no existe en la ruta y la modificación de un archivo existente si el reporte ya existe, lo cual es útil en caso de que algunos datos del DataSet cambien. La limitación es que el usuario tendría que ser muy ordenado con el manejo de los reportes para no mezclar reportes con DataSets que no les corresponden. Se podría arreglar haciendo que el nombre del reporte creado cambie para cada DataSet, capturando en una variable el nombre del DataSet e introduciendo esa variable en el nombre del reporte a crear.

2. ```contenido_informe``` se genera a través de utilizar la clase sobre el df a analizar a través del método de clase generar_reporte(). No se llama ```self.df```, pues ese atributo es propio de la clase y acá se está ejecutando el script por fuera de la misma. En realidad, df viene de la rama else de este bloque if __main__, pues ```df=sys.argv[1]```. Lo que devuelve el método generar_reporte() se verá más adelante.

3. Se usa ```.write()```sobre "ejemplo", es decir, el nombre variable que se le dio al archivo a crear. El argumento que recibe ```.write()```es el contenido_informe capturado en el paso anterior. No se usa este ```.write()``` como el return del método generar_reporte(), primero, para mantener las responsabilidades separadas (es decir, qué hace cada parte del script) y, segundo, porque por allí devolvería el conteo de caracteres y no el reporte propiamente dicho. ```.write()``` siempre devuelve dos cosas: el conteo de caracteres y, al mismo tiempo, escribe sobre el archivo lo que reciba como argumento. Ya veremos más adelante esto último.

**Iteración:**
Se cambió ```sys.exit()``` por ```sys.exit(1)``` para no terminar con un código de ejecución 0, que equivale a ejecución exitosa.

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
## **Explicación del código:**
1. Definición de la clase.
2. Definición de los parámetros de la clase.

Son dos los archivos con los que trabajará este _script_: .csv, .xlsx, aunque la base del procesamiento son los DataFrames. A continuación, en lugar de explicar línea por línea, se explica el funcionamiento general del bloque if:

3. Se comprueba, en primer término, si el argumento pasado a la función NO es de tipo pd.DataFrame. Exactamente eso es lo que hace la tercera línea de código. De ahí, se desprenden dos caminos que funcionan igual:
    - Si el sufijo de df es .csv (cuarta línea), entonces ```df = pd.read_csv(df)``` (sexta línea).
    - Si el sufijo es .xlsx, entonces ```df = pd.read_excel(df)``` (novena línea).
En cualquier caso, se captura ```self.source = df```(quinta y octava líneas) antes de convertir a DataFrame. De esta manera, self.source conserva el str que contiene el argumento exacto que se le dio a la clase.

Cabe aclarar que si ninguno de los dos casos anteriores se cumple, es decir, que el argumento pasado no sea una ruta que termine en .csv o .xlsx, se detiene el constructor de la función con un mensaje de error (décima y undécima líneas).

4. Si el argumento pasado ya es un pd.DataFrame, entonces ```self.source = "DataFrame en memoria"``` (décimotercera línea) y ```df = pd.DataFrame(df)```(décimo cuarta línea).

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
## **Explicación del código:**
1. Se define el método __repr__.
2. Se construye lo que devuelve este método. En este caso, se desea visualizar las características destacables del argumento con el que se construyó la clase:
    - fuente, es decir, si la fuente fue un archivo .csv, .xlsx o un DataFrame. Nótese que se usa !r, pues lo que contiene ```self.source``` es tipo str.
    - filas, es decir, cuántas filas tiene el DataFrame (para este punto, ya df se transformó a un DataFrame).
    - columnas, es decir, cuántas columnas tiene el DataFrame.

# Método reporte_nulos():

La idea es evaluar cuántos datos tipo NaN, NaT y None hay en el DataFrame.

```python
    def reporte_nulos(self):        #primera línea
        return self.df.isna().sum() #segunda línea
```
## **Explicación del código:**
1. Se define el método reporte_nulos().
2. Sobre el atributo ```self.df``` se usa la función ```.isna()```para determinar cuántos valores del DataFrame son NaN, NaT o None. Algunas precisiones importantes sobre ```.isna()```son:
    - Esta función opera sobre cada uno de los valores del DataFrame. Devuelve una dato tipo pd.DataFrame a modo de máscara booleana donde se marcan con True aquellos valores NaN, NaT o None, y con False aquellos que no lo son.
    - Funciona exactamente igual a ```.isnull()```, es decir, son la misma función. Incluso, la documentación oficial dice que esta última es un alias de la primera.
    - ```.sum()``` opera sobre la máscara booleana. Como True es igual a 1 y False es igual a 0, el resultado es un int que representa el número total de valores que son NaN, NaT o None. ```.sum()``` puede recibir el parámetro axis, el cual modifica la dirección de conteo. Por defecto, su valor es igual a 0, lo que significa que cuenta por columnas, es decir, devuelve una sumatoria de los valores de cada columna; axis igual a 1, por el contrario, devuelve una sumatoria total de los valores por fila.

# Método reporte_duplicados():

Sirve para evaluar las filas duplicadas dentro del DataFrame.

```python
    def reporte_duplicados(self):           #primera línea
        return self.df.duplicated().sum()   #segunda línea
```
## **Explicación del código:**
1. Se define el método reporte_duplicados().
2. Sobre el atributo ```self.df``` se usa la función ```.duplicated()``` para determinar cuántas filas exactamente iguales (es decir, con los mismos valores en las mismas columnas) hay. Esta función opera al nivel de la fila y lo que hace es comparar una por una, sin importar si son adyacentes o no, para determinar cuáles de ellas son duplicadas. Como la función devuelve un dato tipo Series a modo de máscara booleana, ```.sum()``` devuelve el total de filas duplicadas con las siguientes consideraciones:
    - Suponiendo que la fila con índice 0 sea exactamente igual a la fila con índice 3, por ejemplo, ```.duplicated()``` marcará la fila con índice 3 como True. Parecería, entonces, que soy hay una fila duplicada cuando en realidad son dos, pero es el comportamiento por defecto de esta función cuando no tiene parámetros (marca como True la fila de índice 3 por ser la duplicada de la fila con índice 0 que, al ser la primera, no es duplicada de ninguna). El parámetro keep es el que determina este comportamiento. Por defecto, es igual a "first". Sin embargo, si es igual a False, marca todas las duplicadas (para el caso, marcaría como True tanto la fila de índice 0 como la fila de índice 3); es útil cuando necesito saber, por ejemplo, el índice de las filas duplicadas. keep también puede ser igual a "last", el cual invierte el comportamiento por defecto (es decir, marcaría la fila con índice 3 como False y la fila con índice 0 como True).
    - Tiene otros parámetros como subset, que sirve para hacer el conteo de duplicados pero restringido a los valores de las columnas indicadas. Por defecto, ```.duplicated()``` opera a nivel de todas las columnas.

## **Iteración del código sobre decisiones de diseño:**

```python
    def reporte_duplicados(self):                                                   #primera línea
        mascara_duplicados = self.df.duplicated(keep=False)                         #segunda línea
        if self.source == "DataFrame en memoria":                                   #tercera línea
            filas_duplicadas = (self.df[mascara_duplicados].index).tolist()         #cuarta línea
            total_duplicadas = int(mascara_duplicados.sum())                        #quinta línea
        else:                                                                       #sexta línea
            filas_duplicadas = (self.df[mascara_duplicados].index + 2).tolist()     #séptima línea
            total_duplicadas = int(mascara_duplicados.sum())                        #octava línea
        return {"total": total_duplicadas, "filas": filas_duplicadas}               #novena línea
```

¿Cuál es el propósito de conocer los duplicados? Si es simplemente saber si existen, el código inicial satisfacía el requerimiento. Pero ¿de verdad es un dato útil? Esta última es la pregunta que generó el cambio de diseño. Conocer qué cantidad de filas hay duplicadas no era un dato especialmente útil, es decir, en términos de requerimientos no funcionales el código era insuficiente. En un DataSet mediano, comparar fila por fila para encontrar cuáles son duplicadas es inviable. 

Así, entonces, la pregunta cambia: ¿se puede actuar y tomar decisiones con un número que solo me indica la cantidad de filas duplicadas que hay? La respuesta es no:
    - Sin sus índices no se pueden comparar para saber el motivo de la duplicación o si de verdad deben estar duplicadas.
    - Sin sus índices, no se pueden eliminar a menos de que se encuentren, lo cual es inviable en un DataSet mediano o grande.

De esta manera, apareció un elemento crucial que el código debía devolver: los índices de las filas duplicadas.

1. Se define el método reporte_duplicados().
2. Se genera una máscara booleana para hallar los duplicados. Se usa el argumento keep=False en ```.duplicated(keep=False)```. Por defecto, keep="first", es decir, marca la primera fila que coincida con una posterior como False y a la segunda como True (lo cual es lógico porque la primera aparición de una fila que se duplica no es duplicada de ninguna). Con ```.duplicated(keep=False)``` se marcan todas las filas que son duplicadas, lo que es útil para conocer sus índices.
3. Si se está analizando un "DataFrame en memoria" (definido así desde el inicio de la clase), se detecta el índice de las filas duplicadas por medio de la aplicación de la máscara booleana a self.df. El resultado se convierte a lista para que se visualice mejor, pues si se mantiene pandas.Index, se muestra el dtype, que es un dato que no le interesa al usuario final.
4. Se hace el conteo del total de elementos duplicados con ```mascara_duplicados.sum()```. Se usa int, pues ```.sum()``` en una máscara booleana devuelve numpy.int64 en el output, lo que es información que no es útil para el usuario. Además, se usa ```.sum()``` sobre la máscara booleana porque las listas y los pandas.Index no tienen atributo ```.sum()```, pero, además, porque al aplicar ```.sum()``` sobre una máscara booleana compuesta de True/False, obtengo exactamente la cantidad de duplicados, pues True == 1 y False == 0.
5. Se aplica la misma lógica en las líneas de código de la sexta a la octava, solo que al índice obtenido se le suman 2 unidades, pues esta es la rama del condicional que sirve para analizar archivos .csv o .xlsx. Estos archivos suelen tener encabezado, entonces el índice de las filas se corre 2 unidades con respecto a un DataFrame, pues en una _spreadsheet_ la primera fila tiene índice 1, no 0, y la fila 1 suele ser el encabezado, entonces los datos reales suelen comenzar desde la fila 2.
6. Se devuelve un diccionario así: "total" es la llave para el valor del total de duplicados; y "filas" es la llave para la lista que contiene el índice de las filas duplicadas.

**Iteración:**
total_duplicados se sacó del bloque if/else, pues solo se debe computar una vez. El código quedó así:

```python
        mascara_duplicados = self.df.duplicated(keep=False)
        total_duplicadas = int(mascara_duplicados.sum())
        if self.source == "DataFrame en memoria":
            filas_duplicadas = (self.df[mascara_duplicados].index).tolist()
        else:
            filas_duplicadas = (self.df[mascara_duplicados].index + 2).tolist()
        return {"total": total_duplicadas, "filas": filas_duplicadas}
```

# Método reporte_tipos_inconsistentes():

Sirve para detectar aquellas columnas que tienen diferentes tipos de datos mezclados.

```python
    def reporte_tipos_inconsistentes(self):                                             #primera línea
        data_columna={}                                                                 #segunda línea
        for col in self.df.columns:                                                     #tercera línea
            data_columna[col]=len(self.df[col].dropna().apply(type).value_counts())     #cuarta línea
        return data_columna                                                             #quinta línea
```
## **Explicación del código:**
1. Se define el método reporte_tipos_inconsistentes().
2. Se define un diccionario que servirá para almacenar la cantidad de tipos de datos que contiene una sola columna, donde la columna es la llave y el conteo de los tipos de datos es el valor. De este modo, si el valor para una llave es mayor a 1, se considera que esa columna es inconsistente.
3. Se declara un ciclo for que usa la variable "col" para recorrer todas las columnas de ```self.df```.
4. El diccionario declarado con cada columna individual como llave se llena con el conteo de los tipos de datos que hay en una columna, así:
    - ```data_columna[col]``` es la declaración donde se define cada columna como llave.
    - ```self.df``` es de tipo pd.DataFrame y se filtra por sus columnas. El ciclo for es indispensable, justamente, para obtener cada columna por iteración. Es decir, sin el ciclo, no se podría evaluar cada columna individualmente.
    - A ```self.df[col]``` se aplica ```.dropna()``` para descartar todos los valores NaN, NaT o None de cada columna, lo cual no solo es importante para no invadir el dominio de la función reporte_nulos(), sino también para no generar datos erróneos en los casos en los que una columna tenga valores tipo str y None (estos últimos también son de tipo float). Por ejemplo, si una columna tiene los valores ["a",None], sin ```.dropna()``` el conteo daría str=1 y float=1, pero None indica simplemente que no hay valor, por lo que no tiene sentido marcar la columna como inconsistente. Eso sería un trabajo para otra función que determine celdas vacías o aparentemente vacías (como aquellas celdas compuestas por solo espacios).
    - Una vez descartados los valores tipo NaN, NaT o None, se aplica a cada columna ```.apply(type)```. La función ```.apply()``` permite aplicarle una función a un objeto tipo pd.DataFrame o pd.Series. Para el caso, lo que se hace aquí es determinar el tipo de cada valor de cada columna. De esta manera, al final, se obtiene un diccionario que contiene un valor tipo int que indica la cantidad de tipos de datos que hay en cada columna. Esta línea sigue el siguiente camino: 
        - ```self.df[col].dropna()``` devuelve un pd.Series sin los valores tipo NaN, NaT, o None que el original tenía.
        - A ese pd.Series se le aplica ```.apply(type)```, lo que devuelve también un pd.Series.
        - A ese pd.Series se le aplica ```.value_counts()```, lo que devuelve también un pd.Series. Es importante esta aclaración: ```.value_counts()``` devuelve los datos únicos y cuántas veces aparecen: por ejemplo, si tengo la lista [1,2,2,2,3,3,4], value_counts() devuelve, por simplificar, algo así: [1:1, 2:3, 3:2, 4:1]. Por su parte, ```.nunique()``` devuelve solo el conteo de datos únicos, para el caso, 4. Es decir, ```len(algo.value_counts())``` es lo mismo que hacer ```algo.nunique()``` para los casos donde solo necesito el conteo de datos únicos y no el desglose de cuántas veces aparece cada uno de esos datos.
        - Ese pd.Series que se obtiene pasa por ```len()```, que devuelve un int como valor por cada llave del diccionario (columnas).
        - Por eso, cuando se afirma que lo que se obtiene es un diccionario, se refiere al resultado final.
    - Aunque de por sí ya es información útil, lo que se necesita no es visualizar el tipo de dato que es cada valor de cada columna, sino cuántos tipos de datos diferentes hay en esa columna. Esta es la pregunta que resuelve ```.value_counts()```.
5. Se define lo que devuelve la función: un diccionario en el que cada llave (en términos prácticos, cada columna) contiene la cantidad de tipos de datos que hay en cada columna de ```self.df```.

## **Intentos fallidos:**
### Primer intento:

```python
def reporte_tipos_inconsistentes(self):
    columns=self.df.columns
    tipos_inconsistentes=self.df[columns].apply(type)
    return tipos_inconsistentes
```
Falla porque ```.apply()``` se comporta diferente según lo que reciba. Cuando recibe un pd.Series, se aplica sobre cada valor individual, pero cuando recibe un pd.DataFrame, se aplica sobre la estructura completa. Como ```columns = self.df.columns```, entonces ```.apply(type)``` recibió mediante ```self.df[columns]``` la totalidad de las columnas. Al realizar la prueba con el siguiente código:

```python
df_prueba = pd.DataFrame({"a": [3,"w",None], "b":[4,"h",0], "c":["x","y","x"]})
columns=df_prueba.columns
tipos_inconsistentes=df_prueba[columns].apply(type)
print(columns)
print(tipos_inconsistentes)
```
Se obtiene lo siguiente:

```python
Index(['a', 'b', 'c'], dtype='str')
a    <class 'pandas.Series'>
b    <class 'pandas.Series'>
c    <class 'pandas.Series'>
dtype: object
```
Esto que quiere decir que evalúa cada columna entera y no cada uno de sus valores. Por eso siempre devuelve pandas.Series

### Segundo intento:

```python
def reporte_tipos_inconsistentes(self):
    for col in self.df.columns:
        return self.df[col].apply(type)
```
Falla porque return corta la ejecución del código una vez se ejecuta su línea. De esta manera, solo devolverá el _output_ para la primera columna.

### Tercer intento:

```python
def reporte_tipos_inconsistentes(self):
    tipos_inconsistentes={}
    for col in self.df.columns:
        tipos_inconsistentes[col]=self.df[col].apply(type)
    return tipos_inconsistentes
```
Funciona, pero no es la versión final. Lo que obtengo es un diccionario que contiene el tipo de dato de cada valor de cada llave, cuando lo que necesito saber es la cantidad de tipos de datos (valor) por columna (llave).

# Método reporte_outliers():

Sirve para detectar los elementos por columna que son outliers, es decir, valores atípicos. Se usa el método intercuartílico para determinar aquellos valores que se encuentran a 1,5 veces del rango intercuartílico (atípicos leves).

```python
    def reporte_outliers(self):                                                     #primera línea
        columnas_numericas = self.df.select_dtypes(include="number").columns        #segunda línea
        Q1 = self.df[columnas_numericas].quantile(0.25)                             #tercera línea
        Q3 = self.df[columnas_numericas].quantile(0.75)                             #cuarta línea
        IQR = Q3 - Q1                                                               #quinta línea
        limite_inferior = Q1 - 1.5 * IQR                                            #sexta línea
        limite_superior = Q3 + 1.5 * IQR                                            #séptima línea
        mascara_outliers = (
            (self.df[columnas_numericas] < limite_inferior)
            | (self.df[columnas_numericas] > limite_superior)
        )                                                                           #octava línea
        valores_outliers = {
            col: self.df[col][mascara_outliers[col]]
            for col in columnas_numericas
        }                                                                           #novena línea
        total_outliers = sum(len(serie) for serie in valores_outliers.values())     #décima línea
        return {"total": total_outliers, "valores": valores_outliers}               #onceava línea
```
## **Explicación del código:**
1. Se define el método reporte_outliers.
2. Se definen las columnas numéricas del DataSet, es decir, aquellas que tienen valores de tipo int64 y float64.
3. Se define el cuartil 1 con ```.quantile()```. Un cuartil consiste en agrupar los datos en 4 grupos, pero con 3 puntos de corte. Estos puntos de corte son:
    - Q1: un valor para el cual el 25 % de los datos están por debajo y el 75 % por encima.
    - Q2: la mediana.
    - Q3: un valor para el cual el 75 % de los datos están por debajo y el 25 % por encima.
De esta manera, se producen 4 grupos: 0-25 %, 25-50 %, 50-75 %, 75-100 %.
4. Se define Q3.
5. Se define el IQR, el cual es la diferencia entre Q3 y Q1.
6. En las dos líneas siguientes se definen el límite inferior y el límite superior. Se usa 1.5 para hallar valores atípicos leves, pues 3 sirve para hallar, sobre todo, los valores atípicos extremos.
7. Se define una máscara booleana para determinar si los valores de las columnas numéricas de self.df son menores al límite inferior definido o mayores al límite superior. Al ser una máscara, obtengo un pd.DataFrame que cataloga cada valor con True si cumple al menos una de las dos condiciones. False si es un valor que no es atípico, es decir, que está dentro del rango.
8. Como pd.DataFrame ya conserva el índice de esos valores atípicos, se crea un diccionario mediante una comprensión, de manera tal que el nombre de la columna sea la llave y los valores aquellos marcados como True por la máscara booleana. A cada columna de self.df se le aplica la máscara booleana pero columna a columna.
9. Cuento cuántos valores son outliers en total.

# Método generar_reporte():

Método orquestador que retoma el _output_ de cada uno de los otros cuatro métodos para organizarlo en un informe legible que luego se condensará en el archivo creado con ```with open``` en el bloque ```if __main__```.

```python
def generar_reporte(self):                                                                                           #primera línea
        duplicadas = self.reporte_duplicados()                                                                       #segunda línea
        cantidad_duplicadas = duplicadas["total"]                                                                    #tercera línea
        if duplicadas["total"] == 0:                                                                                 #cuarta línea
            duplicadas = "Sin filas duplicadas"                                                                      #quinta línea
        else:                                                                                                           
            duplicadas = pd.DataFrame(duplicadas["filas"], columns=["Fila"])                                         #sexta, séptima líneas

        resultado_inconsistentes = self.reporte_tipos_inconsistentes().items()                                       #octava línea
        inconsistentes = pd.Series({col: cantidad for col, cantidad in resultado_inconsistentes if cantidad > 1})    #novena línea

        outliers = self.reporte_outliers()                                                                           #décima línea
        cantidad_outliers = outliers["total"]                                                                        #decimoprimera línea
        lista_filas_outliers=[]                                                                                      #decimosegunda línea
        if outliers["total"] == 0:                                                                                   #decimotercera línea
            outliers = "Sin outliers"                                                                                #decimocuarta línea
        else:                                                                                                        #decimoquinta línea
            for col, serie in outliers["valores"].items():                                                           #decimosexta línea
                for fila, valor in serie.items():                                                                    #decimonovena línea
                    lista_filas_outliers.append({"Columna": col, "Fila": fila, "Valor": valor})                      #vigésima línea
            lista_filas_outliers=pd.DataFrame(lista_filas_outliers)                                                  #vigesimoprimera línea


        informe = (f"""# Metadata:
- Archivo analizado: {self.source}

# Reporte de datos nulos:
{self.reporte_nulos()}

# Reporte de datos duplicados:
**- Cantidad de filas duplicadas:** {cantidad_duplicadas}
**- Filas duplicadas:**
{duplicadas}

# Reporte de tipos inconsistentes:
{inconsistentes}

# Reporte de outliers:
**- Total de outliers:** {cantidad_outliers}
**- Columna, fila y valor de los outliers:**
{lista_filas_outliers}""")

        return informe                                                                                              #líneas restantes
```
## **Explicación del código:**
1. Se define el método generar_reporte().
2. Como reporte_nulos() genera un pd.Series que ya es útil por sí mismo, este método pudo volcarse directamente en la variable "informe". Por lo mismo, generar_reporte() comienza operando sobre el resultado de reporte_duplicados(), así:
    - Se guarda el resultado del método reporte_duplicados() en la variable "duplicadas", de manera tal que esta variable sirva para operar con el diccionario que este método devuelve sin tener que llamar otra vez al método en sí. Se llama una vez y se preserva su resultado en una variable.
    - Antes de que la variable definida anteriormente reciba cualquier transformación, se guarda la cantidad de filas duplicadas en la variable "cantidad_duplicadas", que será útil después para el reporte.
    - Como lo que devuelve reporte_duplicados() es un dict que tiene como llave "total" para el valor de la cantidad de filas duplicadas, si esa llave guarda 0 valores, entonces no hay filas duplicadas y duplicadas = "Sin filas duplicadas".
    - De lo contrario, se filtra el diccionario que devuelve reporte_duplicados() para visualizar solo los valores de su llave "filas", la cual guarda el índice de las filas duplicadas. Este filtro se convierte en un DataFrame con la columna "Fila", en la cual se muestran las filas duplicadas.
¿Por qué no se generó un DataFrame con el diccionario completo que devuelve generar_reporte()? Porque la llave "total" solo contiene un valor tipo int, y la llave "filas" contiene una lista. Al convertir esto a DataFrame, se genera una tabla con las columnas "total" y "filas" con el mismo largo de los datos almacenados en la llave "filas". En la columna "filas", cada fila contendrá, correctamente, el indice de las filas duplicadas, pero en la columna "total" todos los valores de cada fila serán el mismo: el número total de filas duplicadas, lo que puede ser confuso para el usuario.
- Diccionario completo a DataFrame:
```python
total  filas
0      4      0
1      4      2
2      4      3
3      4      4
```
- Diccionario filtrado a DataFrame:
```python
    Fila
0     0
1     2
2     3
3     4
```
3. Para el reporte_tipos_inconsistentes() se manejó así:
    - Como reporte_tipos_inconsistentes() devuelve un dict con cada columna de self.df como llave y la cantidad de tipos de datos únicos que tiene esa columna.
    - Ese dato debe ser filtrado. Para ello, desempaqueto el diccionario en tuplas (llave-valor) a través de ```.items()```.
    - Lo anterior me permite generar una comprensión de diccionario con la columna como llave y la cantidad (valor de la tupla) como valor a través de la iteración de las tuplas que obtuve en el paso anterior. La condición es que si cantidad (valor) > 1, entonces conserve esa tupla, de lo contrario, la descarta, pues si una columna solo tiene un total de datos inconsistentes == 1, quiere decir que no hay tipos de datos mezclados y, por tanto, no es inconsistente.
    - Ese nuevo diccionario generado se convierte de una vez a pd.Series para su correcta visualización.

4. Para el manejo de reportes_outliers() se procedió así:
    - Se guardó el resultado de reporte_outliers() en la variable outliers para no tener que invocar al método cada que vez que se quisiera operar sobre su resultado.
    - Se guardó la cantidad de outliers en la variable cantidad_outliers. Un procedimiento similar a lo que se hizo con duplicados.
    - Se generó una lista con la fila de los outliers y su valor, así:
        - Si la cantidad de totales de outliers en la llave "total" del dict generador por el método reporte_outliers es 0, entonces outliers = "Sin outliers".
        - De lo contrario, del resultado de reporte_outliers() guardado en outliers, utilizo la llave "valores" para obtener un diccionario solo con "valores" como llave. Esa llave guarda una Series que contiene el índice y el valor de los outliers por cada columna. Después, a través de .items(), obtengo una Series que representa el índice de cada outlier y su valor por columna (llave). La lógica es que un DataFrame es tipo pd.DataFrame, pero cada columna de ese DataFrame es una Series. De por sí, valores_outliers es un dict que contiene "col" como llave, pero como la máscara booleana se aplica sobre cada columna individual, la máscara devuelve pd.Series, lo que quiere decir que cada llave contiene una Series como valor, compuesta por el índice y el valor del outliers. outliers["valores"] es un diccionario, pero cuando le aplico .items(), obtengo su llave "col" y sus valores "serie", que son una Series. Es importante considerar que .items() siempre devuelve una tupla (llave, valor), pero como en el primer ciclo for sucede que valor es una Series, por eso en este caso particular el segundo valor de la tupla es una Series.
        - De esta manera, "serie" en el primer ciclo for es la Series que contiene el índice de la fila con el outlier y el valor del outlier por columna.
        - A través de .items() en este nivel, el segundo ciclo for desempaqueta esa Series en tuplas y le asigna fila, valor como sus variables.
        - Luego genero un diccionario con tres llaves y sus valores:
            - "Columna": col, recuperado el valor del primer ciclo for.
            - "Fila": fila, recuperado el valor del segundo ciclo.
            - "Valor": valor, recuperado del segundo ciclo.

5. informe simplemente es la variable que contiene el reporte formateado como texto. Se usan triple comillas para que la indentación no sea un problema, pues si no se hace así, el reporte queda tabulado con la misma indentación de Python, lo cual se podría resolver también con textwrap.dedent()
6. La función devuelve informe, que es de donde el bloque if __main__ en with open captura la información para generar el archivo.

**Iteración:**
Después de:
```python
       resultado_inconsistentes = self.reporte_tipos_inconsistentes().items()                                       
        inconsistentes = pd.Series({col: cantidad for col, cantidad in resultado_inconsistentes if cantidad > 1}) 
```
Se añadieron las líneas:
```python
if inconsistentes.empty:
    inconsistentes = "Sin tipos inconsistentes"
```
Con el fin de proporcionarle un dato útil al usuario en vez de una serie vacía.

# pytest

A continuación, se describe el código de pytest.

**Notas:** se usa conftest.py desde la carpeta principal del proyecto (en la que se aloja data_profiler.py, es decir, el pipeline completo) para que Python pueda importar su contenido a test_data_profiler.py, que se encuentra en data-quality_profiler/tests.

## imports y decoradores fixture:

```python
import pandas as pd                                                 #primera línea
import pytest                                                       #segunda línea

from data_profiler import DataProfiler                              #tercera línea

@pytest.fixture(scope = "module")                                   #cuarta línea
def dataframe_test():                                               #quinta línea
    df = pd.DataFrame({"a": [1, 2, 1, pd.NA, 3, 4, 5, 6],           #sexta línea
                       "b": [1, 3, 1, "z", 5, 6, 7, 8], 
                       "c": [1, 4, 1, 7, 2, 3, 4, 5], 
                       "d": [10, 11, 10, 9, 12, 8, -50, 100]
                       })
    return df                                                       #séptima línea

@pytest.fixture(scope = "module")                                   #octava línea
def profiler(dataframe_test):                                       #novena línea
    profiler = DataProfiler(dataframe_test)                         #décima línea
    return profiler                                                 #undécima línea
```
### **Explicación del código:**
1. De la línea 1 a la 3 se hacer los imports necesarios para los tests.
2. Se define el decorador fixture con scope = "module".
    - ¿Por qué un fixture? Los fixture son una herramienta que permite "fijar" un caso de prueba que puede ser reutilizado por cuantos tests lo necesiten, de manera que se evita tener que introducir el input de prueba a mano por test. En términos simples: se construye un caso de prueba una sola vez que se puede reutilizar a conveniencia sin tener que hardcodear el mismo caso varias veces.
    - ¿Y por qué no una variable? Porque las variables funcionan a nivel del módulo y cada test puede introducir una mutación sobre ella. Si defino la variable X, por ejemplo, y la utilizo en un test que la mute, obtendré la variable X diferente a la original. Si en el test siguiente introduzco X, en realidad el input es el resultado del test anterior. En otro sentido, una variable no resuelve el problema de los casos de prueba que se deben reusar.
    - ¿Y el scope? Son 3:
        - "function": funciona a nivel de cada función definida. Evita la mutación del objeto original, pues este se reconstruye tantas veces como tests lo utilicen. Es útil cuando cada test necesita el input original. Su desventaja radica en el tiempo de ejecución: al tener que reconstruir el objeto varias veces, aquel se puede ver afectado.
        - "module": funciona a nivel del módulo. No evita la mutación del objeto original. El objeto original se construye una sola vez y cada test puede introducir una mutación en el mismo, de manera que un test posterior a uno que haya mutado el objeto original, recibirá la versión mutada de este último. Es útil cuando ninguno
        - "session": funciona igual a "module", pero a nivel de la sesión.
        - Entonces ¿por qué "module" para esta prueba?: porque ninguno de los métodos de la clase DataProfiler muta el objeto original, por lo que "module" es seguro: cada test recibirá una copia fresca del objeto sin los peligros de la mutación. Para el caso, su ventaja radica en el tiempo de ejecución, pues el objeto se construye una sola vez.
3. Se define la función que construye el objeto de prueba.
4. Se construye un DataFrame con casos conocidos: 2 filas duplicadas, 2 valores outliers, 1 columna con tipos inconsistentes y 1 valor nulo.
5. Esta función devuelve el objeto creado.
6. Se construye otro fixture con scope = "module" por las razones ya explicadas. Este es un fixture anidado que se construye con lo retornado por el fixture anterior.
7. Se define la función profiler con el parámetro que devolvió la función anterior. La sintaxis ```def profiler(dataframe_test):``` no significa que profiler llame y ejecute directamente a la función anterior. Nunca se llama directamente a la función, sino al valor que retorna.
8. Esta función crea la variable profiler, la cual contiene la clase DataProfiler aplicada al DataFrame de prueba.
9. La función devuelve profiler.

## def test_reporte_nulos y def test_no_muta_original_nulos:

```python
def test_reporte_nulos(profiler):                                       #primera línea
    serie_nulos = profiler.reporte_nulos()                              #segunda línea
    total_nulos = sum(value for label, value in serie_nulos.items())    #cuarta línea
    assert total_nulos == 1                                             #quinta línea

def test_no_muta_original_nulos(profiler, dataframe_test):              #sexta línea
    dataframe_test_copy = dataframe_test.copy()                         #séptima línea
    profiler.reporte_nulos()                                            #octava línea
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)  #novena línea
```
### **Explicación del código:**
1. Se define el test para probar el método reporte_nulos() de DataProfiler.
2. reporte_nulos() devuelve un objeto pandas.Series que se captura en la variable serie_nulos, la cual es el resultado de aplicar el método reporte_nulos() al fixture profiler.
3. Para saber si el método funciona o no, no es necesario hacer assert del resultado total de reporte_nulos(), sino solo del total de nulos que devuelve. El objeto construído para esta prueba tiene un solo valor nulo.
4. Se captura el total de nulos en serie_nulos, es decir, se omite el índice.
5. Se compara el valor capturado en total_nulos con 1, que es exactamente la cantidad de nulos que tiene el objeto original.
6. Se construye otro test para demostrar que reporte_nulos() no muta el objeto original. Sus parámetros son los valores devueltos por las funciones fixture definidas al comienzo.
7. Se genera una copia del objeto original.
8. Se ejecuta el método reporte_nulos() sobre profiler. No se guarda en nada, pues para el test no interesa el resultado, solo que se ejecute para demostrar que el objeto original no muta.
9. Se compara el objeto original con su copia. Si reporte_nulos() hubiera mutado el objeto original, dataframe_test sería diferente a su copia y el test fallaría. De aquí en adelante, la comprobación de no-mutación se simplifica.

**La filosofía del test es probar el caso mínimo que garantiza que todo funciona correctamente. En este caso, por ejemplo, si el total es igual a 1 es imposible que el índice este mal, pues en todo el DataFrame de prueba solo hay un valor nulo en una posición fija, inmutable. No se necesita, por tanto, comprobar el índice. Es posible que esta filosofía no se haya segudio al pie de la letra en los demás tests, pero se justifica como práctica de sintaxis y de entender qué tipo de objeto devuelve cada método de DataProfiler.**

## def test_reporte_duplicados:

```python   
def test_reporte_duplicados(profiler, dataframe_test):                  
    dataframe_test_copy = dataframe_test.copy()                         
    resultado = profiler.reporte_duplicados()                           
    assert resultado == {"total": 2, "filas": [0, 2]}                   
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)  
```
### **Explicación del código:**
No es necesario detenerse en la explicación de este código, pues puede entenderse como una unión del test anterior: se compara el resultado del método reporte_duplicados() sobre profiler con los casos conocidos del DataFrame original y, al mismo tiempo, se comprueba que reporte_duplicados() no muta el objeto.

## def test_reporte_tipos_inconsistentes:

```python
def test_reporte_tipos_inconsistentes(profiler, dataframe_test):
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_tipos_inconsistentes()
    assert resultado == {"a": 1, "b": 2, "c": 1, "d": 1}
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)
```
### **Explicación del código:**
Al igual que el anterior, no es necesario detenerse en la explicación.

## def test_reporte_outliers:

```python
def test_reporte_outliers(profiler, dataframe_test):                                                                #primera línea
    dataframe_test_copy = dataframe_test.copy()                                                                     #segunda línea
    resultado = profiler.reporte_outliers()                                                                         #tercera línea
    assert resultado["total"] == 2                                                                                  #cuarta línea
    pd.testing.assert_series_equal(resultado["valores"]["c"], pd.Series([], name = "c", dtype = "int64"))           #quinta línea
    pd.testing.assert_series_equal(resultado["valores"]["d"], pd.Series([-50, 100], name = "d", index = [6, 7]))    #sexta línea
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)                                              #octava línea
```
### **Explicación del código:**
Este sí es un caso especial que requiere explicación:
1. Se define el test para el método reporte_outliers() con dos parámetros.
2. Se genera una copia del DataFrame original.
3. Se compara el resultado (filtrado por la llave "total" del diccionario que construye reporte_outliers) de aplicar reporte_outliers() sobre profiler con los 2 valores conocidos de outliers en el DataFrame original.
4. En lo sucesivo, es importante entender lo que devuelve reporte_outliers(): un diccionario con dos llaves:
    - "total": cuyo valor es el total de outliers del DataFrame original.
    - "valores: que a su vez se compone de un diccionario cuyas llaves son las columnas donde se encontraron los outliers y sus valores son pandas.Series que contiene el índice del outlier y su valor.
    - Además, y muy importante, todo el funcionamiento de reporte_outliers() se basa en que SOLO analiza las columnas numéricas del DataFrame original, es decir, aquellas cuyo dtype es un número. Esto quiere decir que cualquier columna numérica aparecerá en lo devuelto por valores_outliers(), incluso si ninguna de esas columnas tiene, en efecto, un outliers, en cuyo caso la Series de la llave es vacía. Esto último genera otro incoveniente para la prueba: si la Series es vacía, su dtype ya no es númerico, sino "object": esto puede hacer que la prueba falle, pues el test también se fija en el dtype para determinar la paridad entre la Series esperada y la Series obtenida.
    - El test, entonces, consiste en que el valor esperado es igual a ```resultado["valores"]["c"]``` del DataFrame de prueba. ¿Por qué es necesaria esta línea? Porque la columna "c" es numérica, aunque no tenga outliers, por eso se compara con una Series vacía en la columna "c" y se fija su dtype a "int64" para que el dtype "object" no haga que el test falle.
    - ¿Y por qué no un ciclo for que construya un diccionario igual al que genera reporte_outliers() y hacer así la comparación? Porque es mucho código para solo dos comparaciones. Es más eficiente escribirlas directamente que plantear esa lógica con for.
5. La misma lógica se aplica en esta línea: la columna "d" sí tiene outliers, por eso se compara con una Series no nula, por la columna "d" y por los índices exactos en los que están esos outliers.
6. Se comprueba que reporte_outliers() no muta el DataFrame original.

## def test_generar_reporte:

```python
def test_generar_reporte(profiler, dataframe_test):                                                             #primera línea
    dataframe_test_copy = dataframe_test.copy()                                                                 #segunda línea
    resultado = profiler.generar_reporte()                                                                      #tercera línea
    assert str(profiler.reporte_nulos())  in resultado                                                          #cuarta línea
    assert f"**- Cantidad de filas duplicadas:** {profiler.reporte_duplicados()["total"]}" in resultado         #quinta línea
    resultado_inconsistentes = profiler.reporte_tipos_inconsistentes().items()                                  #sexta línea
    inconsistentes = pd.Series({col: cantidad for col, cantidad in resultado_inconsistentes if cantidad > 1})   #séptima línea
    assert str(inconsistentes) in resultado                                                                     #octava línea
    assert f"**- Total de outliers:** {profiler.reporte_outliers()["total"]}" in resultado                      #novena línea
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)                                          #décima línea
```
### **Explicación del código:**
1. Sobra explicar las tres primeras líneas.
2. Como generar_reporte() devuelve un str completo, lo que se compara es que cada método devuelve algo que constituya una cadena de texto en cualquier lugar de lo que devuelve generar_reporte().
3. El caso de duplicados es especial, pues es comparar un int que puede aparecer en cualquier lugar de lo devuelto. Si ese int está en cualquier posición del resultado, entonces el test pasa, pero eso no garantiza que ese valor estuviera en la posición correcta. Por eso se añadió el contexto ```f"**- Cantidad de filas duplicadas:**```.
4. Inconsistentes también es un caso especial. En vez de reconstruir exactamente como cadena de texto el resultado de reporte_tipos_inconsistentes(), obtengo un valor representativo del mismo y lo busco en resultado.
5. La lógica de outliers es la misma del punto 3.
6. Se compara que ninguno de estos 5 métodos muta el DataFrame original.

**En este caso, la filosofía no es reconstruir a mano lo que devuelve generar_reporte(), pues es tedioso en la medida en que tengo que reconstruir todo el informe a mano. Más bien, se compara casos representativos que demuestren que el método funciona. La filosofía del caso mínimo de prueba.**