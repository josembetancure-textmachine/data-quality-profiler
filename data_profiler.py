import sys
import pandas as pd
from pathlib import Path


class DataProfiler:
    '''
    Contiene un DataFrame y 5 métodos distintos que se usan para analizar la calidad de los datos de ese DataFrame.

    Attributes:
        df (pandas.DataFrame): DataFrame construido desde su formato de origen.
        source (str): contiene la ruta de origen del DataFrame si proviene de un archivo .csv o .xlsx o el str "DataFrame en memoria" si se construye 
        directamente como pandas.DataFrame para su análisis.
    '''

    def __init__(self, df):
        '''
        Inicializa un objeto DataProfiler según su origen (.csv, .xlsx o "DataFrame en memoria").

        Args:
            df (str, pandas.DataFrame): cadena de texto que contiene la ruta de origen del archivo .csv o .xlsx que dará origen al pandas.DataFrame. O directamente
            pandas.DataFrame si se pasa un DataFrame ya construido.
        
        Raises:
            ValueError: si el objeto pandas.DataFrame proviene de un archivo que no sea .csv, .xlsx ni un DataFrame construido directamente como pandas.DataFrame.
            FileNotFoundError: si la ruta pasada no lleva a ningún archivo.
        '''
        if not isinstance(df, pd.DataFrame):
            if Path(df).suffix == ".csv":
                self.source = df
                df = pd.read_csv(df)
            elif Path(df).suffix == ".xlsx":
                self.source = df
                df = pd.read_excel(df)
            else:
                raise ValueError("La ruta del archivo a analizar contiene un error o es un formato no admitido."
                                 " Solo se admiten formatos .csv, .xlsx y DataFrames."
                                 )
        else:
            self.source = "DataFrame en memoria"
            df = pd.DataFrame(df)

        self.df = df

    def __repr__(self):
        '''
        Devuelve una representación legible del objeto para debugging.

        Returns:
            str: cadena donde se indica la fuente del DataFrame a analizar y su cantidad de filas y columnas.
        '''
        return f"DataProfiler(fuente={self.source!r}, filas={len(self.df)}, columnas={len(self.df.columns)})"

    def reporte_nulos(self):
        '''
        Método para contabilizar la cantidad de datos nulos (NaN, NaT o None) en self.df

        Returns:
            pandas.Series: contiene la cantidad de datos nulos (NaN, NaT o None) por columna de self.df
        '''
        return self.df.isna().sum()

    def reporte_duplicados(self):
        '''
        Método para contabilizar la cantidad de filas duplicadas en self.df y ubicar sus índices.

        Returns:
            dict: llave "total" para la cantidad de filas duplicadas, llave "filas" para la lista con los índices de las filas duplicadas si self.source = "DataFrame en 
            memoria", o cada índice +2 si self.source es un archivo .csv o .xlsx.
        '''
        mascara_duplicados = self.df.duplicated(keep=False)
        total_duplicadas = int(mascara_duplicados.sum())
        if self.source == "DataFrame en memoria":
            filas_duplicadas = (self.df[mascara_duplicados].index).tolist()
        else:
            filas_duplicadas = (self.df[mascara_duplicados].index + 2).tolist()
        return {"total": total_duplicadas, "filas": filas_duplicadas}

    def reporte_tipos_inconsistentes(self):
        '''
        Método para contabilizar la cantidad de tipos de datos (después de descartar los valores nulos) que hay por cada columna de self.df

        Returns:
            dict: la llave es cada columna en self.df y su valor es la cantidad de tipos diferentes de datos que hay en esa columna.
        '''
        data_columna = {}
        for col in self.df.columns:
            data_columna[col] = len(self.df[col].dropna().apply(type).value_counts())
        return data_columna

    def reporte_outliers(self):
        '''
        Método para contabilizar la cantidad de outliers que hay en self.df y encontrar cuáles son y su ubicación según el método intercuartílico. 

        Returns:
            dict: llave "total" que contiene un int que representa la cantidad de outliers en self.df  y llave "valores" que representa un dict que
            tiene como llave cada columna de self.df que sea numérica. A su vez, cada valor de esta llave representa un pandas.Series que contiene el índice del outlier
            dentro de esa columna (llave) y su valor, o vacío si la columna es numérica sin outliers.
        '''
        columnas_numericas = self.df.select_dtypes(include="number").columns
        Q1 = self.df[columnas_numericas].quantile(0.25)
        Q3 = self.df[columnas_numericas].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        mascara_outliers = (
            (self.df[columnas_numericas] < limite_inferior)
            | (self.df[columnas_numericas] > limite_superior)
        )
        valores_outliers = {
            col: self.df[col][mascara_outliers[col]]
            for col in columnas_numericas
        }
        total_outliers = sum(len(serie) for serie in valores_outliers.values())
        return {"total": total_outliers, "valores": valores_outliers}

    def generar_reporte(self):
        '''
        Método orquestador que compila los datos de los demás métodos en un solo reporte legible en formato .md

        Returns:
            str: cadena de texto que presenta de manera legible la información devuelta por cada uno de los demás métodos.
            Para el caso de los tipos inconsistentes, se presentan en el informe únicamente las columnas que contienen 2 o más tipos de datos;
            para el caso de outliers, se convierte la información en un DataFrame legible con las columnas "Columna", "Fila" y "Valor" para visualizar los datos
            más fácilmente.
        '''
        duplicadas = self.reporte_duplicados()
        cantidad_duplicadas = duplicadas["total"]
        if duplicadas["total"] == 0:
            duplicadas = "Sin filas duplicadas"
        else:
            duplicadas = pd.DataFrame(duplicadas["filas"], columns=["Fila"])

        resultado_inconsistentes = self.reporte_tipos_inconsistentes().items()
        inconsistentes = pd.Series({col: cantidad for col, cantidad in resultado_inconsistentes if cantidad > 1})
        if inconsistentes.empty:
            inconsistentes = "Sin tipos inconsistentes"

        outliers = self.reporte_outliers()
        cantidad_outliers = outliers["total"]
        lista_filas_outliers=[]
        if outliers["total"] == 0:
            outliers = "Sin outliers"
        else:
            for col, serie in outliers["valores"].items():
                for fila, valor in serie.items():
                    lista_filas_outliers.append({"Columna": col, "Fila": fila, "Valor": valor})
            lista_filas_outliers=pd.DataFrame(lista_filas_outliers)


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

        return informe

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Falta almenos un argumento. Debe ejecutar la herramienta así:\npython3 data_profiler.py archivo_a_analizar(con su extensión)")
        sys.exit(1)
    else:
        df = sys.argv[1]

        with open("ejemplo_reporte.md","w") as ejemplo:
            contenido_informe = DataProfiler(df).generar_reporte()
            ejemplo.write(contenido_informe)