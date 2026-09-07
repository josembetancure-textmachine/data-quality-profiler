# Contexto

Este proyecto surgió como etapa inicial de mi camino de aprendizaje autónomo, el cual abarca Python, pandas, SQL, PyTorch y demás herramientas que me permitan dedicarme a NLP en un lapso de 2 años.

Ante el uso de la IA como generadora de código, estas notas pretenden, primero, ser una evidencia de mi proceso de pensamiento a medida que construía el código y, segundo, demostrar que interioricé los conceptos usados. Por supuesto, me apoyé en Claude como "instructor particular" para que me explicara qué debía usar, cómo y cuándo, mas no le asigné el rol de programador activo mediante _prompting_ o _vibe coding_. Todo lo construido en este proyecto fue hecho por mí.

**De ser necesario, cada sección contendrá un apartado para explicar los intentos fallidos de código con el objetivo de consolidar mejor el aprendizaje.**

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
## **Explicación del código:**
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
## **Explicación del código:**

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
## **Explicación del código:**

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
## **Explicación del código:**

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
## **Explicación del código:**

1. Se define el método reporte_duplicados().
2. Sobre el atributo ```self.df``` se usa la función ```.duplicated()``` para determinar cuántas filas exactamente iguales (es decir, con los mismos valores en las mismas columnas) hay. Esta función opera al nivel de la fila y lo que hace es comparar una por una, sin importar si son adyacentes o no, para determinar cuáles de ellas son duplicadas. Como la función devuelve un dato tipo Series a modo de máscara booleana, ```.sum()```devuelve el total de filas duplicadas con las siguientes consideraciones:
    - Suponiendo que la fila con índice 0 sea exactamente igual a la fila con índice 3, por ejemplo, ```.duplicated()``` marcará la fila con índice 3 como True. Parecería, entonces, que soy hay una fila duplicada cuando en realidad son dos, pero es el comportamiento por defecto de esta función cuando no tiene parámetros (marca como True la fila de índice 3 por ser la duplicada de la fila con índice 0 que, al ser la primera, no es duplicada de ninguna). El parámetro keep es el que determina este comportamiento. Por defecto, es igual a "first". Sin embargo, si es igual a False, marca todas las duplicadas (para el caso, marcaría como True tanto la fila de índice 0 como la fila de índice 3); es útil cuando necesito saber, por ejemplo, el índice de las filas duplicadas. keep también puede ser igual a "last", el cual invierte el comportamiento por defecto (es decir, marcaría la fila con índice 3 como False y la fila con índice 0 como True).
    - Tiene otros parámetros como subset, que sirve para hacer el conteo de duplicados pero restringido a los valores de las columnas indicadas. Por defecto, ```.duplicated()``` opera a nivel de todas las columnas.

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
        - A ese pd.Series se le aplica ```.value_counts()```, lo que devuelve también un pd.Series.
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
Falla porque ```.apply()``` se comporta diferente según lo que reciba. Cuando recibe un pd.Series, se aplica sobre cada valor individual, pero cuando recibe un pd.DataFrame, se aplica sobre la estructura completa. Como ```columns=self.df.columns```, entonces ```.apply(type)``` recibió mediante ```self.df[columns]``` la totalidad de las columnas. Al realizar la prueba con el siguiente código:
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
    