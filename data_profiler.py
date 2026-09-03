import sys
import pandas as pd
from pathlib import Path

class DataProfiler:
    def __init__(self,df):

        if not isinstance(df,pd.DataFrame):
            if Path(df).suffix==".csv":
                self.source=df
                df=pd.read_csv(df)
            elif Path(df).suffix==".xlsx":
                self.source=df
                df=pd.read_excel(df)
            else:
                raise ValueError("La ruta del archivo a analizar contiene un error o es un formato no admitido."
                                 " Solo se admiten formatos .csv, .xlsx y DataFrames."
                                 )
        else:
            self.source="DataFrame en memoria"
            df=pd.DataFrame(df)

        self.df=df

    def __repr__(self):
        return f"DataProfiler(fuente={self.source!r}, filas={len(self.df)}, columnas={len(self.df.columns)})"

    def reporte_nulos(self):
        return self.df.isna().sum()

    def reporte_duplicados(self):
        mascara_duplicados=self.df.duplicated(keep=False)
        if self.source=="DataFrame en memoria":
            filas_duplicadas=(self.df[mascara_duplicados].index).tolist()
            total_duplicadas=int(mascara_duplicados.sum())
        else:
            filas_duplicadas=(self.df[mascara_duplicados].index+2).tolist()
            total_duplicadas=int(mascara_duplicados.sum())
        return {"total":total_duplicadas, "filas":filas_duplicadas}

    def reporte_tipos_inconsistentes(self):
        data_columna={}
        for col in self.df.columns:
            data_columna[col]=len(self.df[col].dropna().apply(type).value_counts())
        return data_columna

    def reporte_outliers(self):
        columnas_numericas=self.df.select_dtypes(include="number").columns
        Q1=self.df[columnas_numericas].quantile(0.25)
        Q3=self.df[columnas_numericas].quantile(0.75)
        IQR=Q3-Q1
        limite_inferior=Q1-1.5*IQR
        limite_superior=Q3+1.5*IQR
        limites=((self.df[columnas_numericas]<limite_inferior)|(self.df[columnas_numericas]>limite_superior)).sum()
        return limites
    
if __name__=="__main__":
    if len(sys.argv)<2:
        print("Falta almenos un argumento. Debe ejecutar la herramienta así:\npython3 data_profiler.py archivo_a_analizar(con su extensión)")
        sys.exit()
    else:
        df=sys.argv[1]