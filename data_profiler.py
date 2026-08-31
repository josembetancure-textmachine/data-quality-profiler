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
                raise ValueError("La ruta del archivo a analizar contiene un error o es un formato no admitido. Solo se admiten formatos .csv, .xlsx y DataFrames.")
        else:
            self.source="DataFrame en memoria"
            df=pd.DataFrame(df)

        self.df=df

    def __repr__(self):
        return f"DataProfiler(fuente={self.source!r}, filas={len(self.df)}, columnas={len(self.df.columns)})"

    def reporte_nulos(self):
        return self.df.isna().sum()

    def reporte_duplicados(self):
        return self.df.duplicated().sum()

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Falta almenos un argumento. Debe ejecutar la herramienta así:\npython3 data_profiler.py archivo_a_analizar(con su extensión)")
        sys.exit()
    else:
        df=sys.argv[1]