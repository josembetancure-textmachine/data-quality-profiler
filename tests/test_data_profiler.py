import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

from data_profiler import MAX_FILAS_REPORTE, DataProfiler

@pytest.fixture(scope = "module")
def dataframe_test():
    '''
    Fixture con scope de módulo que construye un DataFrame de prueba con propiedades de calidad de datos conocidas de antemano: un valor nulo (columna "a"),
    dos filas duplicadas (índices 0 y 2), tipos inconsistentes (columna "b" mezcla int y str) y dos outliers según el método intercuartílico (columna "d": -50 y 100).
    La columna "c" es numérica limpia, sin outliers, como caso de contraste.

    Se comparte entre todos los tests del módulo (scope="module") porque ningún método de DataProfiler muta self.df, así que reconstruirlo en cada test sería innecesario.

    Returns:
        pandas.DataFrame: DataFrame de prueba con las propiedades descritas arriba.
    '''
    df = pd.DataFrame({"a": [1, 2, 1, pd.NA, 3, 4, 5, 6], 
                       "b": [1, 3, 1, "z", 5, 6, 7, 8], 
                       "c": [1, 4, 1, 7, 2, 3, 4, 5], 
                       "d": [10, 11, 10, 9, 12, 8, -50, 100]
                       })
    return df

@pytest.fixture(scope = "module")
def profiler(dataframe_test):
    '''
    Fixture con scope de módulo que construye una instancia de DataProfiler a partir de dataframe_test, para no repetir su construcción en cada test.

    Args:
        dataframe_test (pandas.DataFrame): fixture que provee el DataFrame de prueba.

    Returns:
        DataProfiler: instancia lista para probar sus métodos de reporte.
    '''
    profiler = DataProfiler(dataframe_test)
    return profiler

def test_reporte_nulos(profiler):
    '''Verifica que reporte_nulos() cuente correctamente el único valor nulo del DataFrame de prueba.'''
    serie_nulos = profiler.reporte_nulos()
    total_nulos = sum(value for label, value in serie_nulos.items())
    assert total_nulos == 1

def test_no_muta_original_nulos(profiler, dataframe_test):
    '''Verifica que llamar a reporte_nulos() no modifique el DataFrame original.'''
    dataframe_test_copy = dataframe_test.copy()
    profiler.reporte_nulos()
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_duplicados(profiler, dataframe_test):
    '''Verifica que reporte_duplicados() identifique las dos filas duplicadas (índices 0 y 2) y no modifique el DataFrame original.'''
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_duplicados()
    assert resultado == {"total": 2, "filas": [0, 2]}
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_tipos_inconsistentes(profiler, dataframe_test):
    '''Verifica que reporte_tipos_inconsistentes() detecte la inconsistencia de tipos en la columna "b" (int y str) y no modifique el DataFrame original.'''
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_tipos_inconsistentes()
    assert resultado == {"a": 1, "b": 2, "c": 1, "d": 1}
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_outliers(profiler, dataframe_test):
    '''Verifica que reporte_outliers() detecte los dos outliers de la columna "d" (-50 y 100), confirme que "c" no tiene outliers, y no modifique el DataFrame original.'''
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_outliers()
    assert resultado["total"] == 2
    pd.testing.assert_series_equal(resultado["valores"]["c"], pd.Series([], name = "c", dtype = "int64"))
    pd.testing.assert_series_equal(resultado["valores"]["d"], pd.Series([-50, 100], name = "d", index = [6, 7]))
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_duplicados_offset_csv(tmp_path):
    '''Verifica que reporte_duplicados() detecte las filas duplicadas del DataFrame original con el offset de +2 cuando se trata de .csv o .xlsx'''
    df_prueba = pd.DataFrame({"a": [1, 2, 1]})  # fila 0 y fila 2 son duplicadas
    archivo = tmp_path / "prueba.csv"
    df_prueba.to_csv(archivo, index=False)
    profiler_csv = DataProfiler(str(archivo))
    resultado = profiler_csv.reporte_duplicados()
    assert resultado == {"total": 2, "filas": [2, 4]}

def test_generar_reporte(profiler, dataframe_test):
    '''Verifica que generar_reporte() incluya los resultados de los cuatro métodos de reporte como Markdown real (tablas y listas), sin modificar el DataFrame original.'''
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.generar_reporte()
    assert re.search(r"\|\s*a\s*\|\s*1\s*\|", resultado)
    assert f"- **Cantidad de filas duplicadas:** {profiler.reporte_duplicados()["total"]}" in resultado
    assert re.search(r"\|\s*b\s*\|\s*2\s*\|", resultado)
    assert f"- **Total de outliers:** {profiler.reporte_outliers()["total"]}" in resultado
    assert re.search(r"\|\s*d\s*\|\s*6\s*\|\s*-50\s*\|", resultado)
    assert re.search(r"\|\s*d\s*\|\s*7\s*\|\s*100\s*\|", resultado)
    assert "dtype:" not in resultado
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_generar_reporte_sin_ruta_local(tmp_path):
    '''Verifica que el reporte muestre solo el nombre del archivo analizado, y no su ruta completa, aunque se pase una ruta absoluta (A-03).'''
    archivo = tmp_path / "prueba.csv"
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(archivo, index=False)
    resultado = DataProfiler(str(archivo)).generar_reporte()
    assert "- Archivo analizado: prueba.csv" in resultado
    assert str(tmp_path) not in resultado

def test_generar_reporte_no_recorta_columnas():
    '''Verifica que, con más de 60 columnas, la tabla de nulos las incluya todas; antes pandas recortaba la sección a 10 filas (H6).'''
    df = pd.DataFrame({f"col_{i}": [1, 2, 3] for i in range(61)})
    df.loc[0, "col_30"] = None
    resultado = DataProfiler(df).generar_reporte()
    assert "col_30" in resultado
    assert ".." not in resultado

def test_generar_reporte_declara_tope_de_filas():
    '''Verifica que, si hay más filas duplicadas que MAX_FILAS_REPORTE, el reporte muestre solo las primeras y lo diga, en vez de recortar en silencio (H6).'''
    df = pd.DataFrame({"a": [1] * 70})
    resultado = DataProfiler(df).generar_reporte()
    assert f"Se muestran las primeras {MAX_FILAS_REPORTE} de 70 filas." in resultado

def test_generar_reporte_offset_outliers_csv(tmp_path):
    '''Verifica que, en el reporte de un .csv, la fila de un outlier lleve el mismo +2 que las filas duplicadas, para que coincida con la fila real del archivo (H7).'''
    df_prueba = pd.DataFrame({"v": [10, 11, 12, 10, 11, 12, 13, 1000]})  # el outlier 1000 tiene índice 7: es la fila 9 del archivo
    archivo = tmp_path / "prueba.csv"
    df_prueba.to_csv(archivo, index=False)
    resultado = DataProfiler(str(archivo)).generar_reporte()
    assert re.search(r"\|\s*v\s*\|\s*9\s*\|\s*1000\s*\|", resultado)

def test_generar_reporte_sin_outliers():
    '''Verifica que, sin outliers, la sección diga "Sin outliers" en vez de imprimir una lista vacía (A-01).'''
    df = pd.DataFrame({"a": [1, 2, 3, 4]})
    resultado = DataProfiler(df).generar_reporte()
    seccion_outliers = resultado.split("# Reporte de outliers:")[1]
    assert "Sin outliers" in seccion_outliers
    assert "[]" not in seccion_outliers

def test_generar_reporte_columnas_evaluadas(profiler):
    '''Verifica que la sección de outliers diga sobre qué columnas numéricas se buscaron (A-06).'''
    resultado = profiler.generar_reporte()
    assert "- **Columnas numéricas evaluadas:** c, d" in resultado

def test_generar_reporte_sin_columnas_numericas():
    '''Verifica que, sin columnas numéricas, el reporte diga que no se buscaron outliers, en vez de mostrar un 0 que parece un resultado (A-06).'''
    df = pd.DataFrame({"texto": ["a", "b", "c"]})
    resultado = DataProfiler(df).generar_reporte()
    assert "- **Columnas numéricas evaluadas:** ninguna" in resultado
    assert "No hay columnas numéricas: no se buscaron outliers." in resultado

def test_extension_en_mayusculas(tmp_path):
    '''Verifica que se acepte un .csv válido aunque su extensión esté en mayúsculas (H9).'''
    archivo = tmp_path / "DATOS.CSV"
    pd.DataFrame({"a": [1, 2, 3]}).to_csv(archivo, index=False)
    profiler_csv = DataProfiler(str(archivo))
    assert len(profiler_csv.df) == 3

def test_cli_error_no_borra_reporte_anterior(tmp_path):
    '''Verifica que, si el análisis falla, el CLI no deje vacío el ejemplo_reporte.md que ya existía (H8).'''
    reporte = tmp_path / "ejemplo_reporte.md"
    reporte.write_text("reporte anterior")
    script = Path(__file__).resolve().parent.parent / "data_profiler.py"
    ejecucion = subprocess.run([sys.executable, str(script), "no_existe.csv"], cwd=tmp_path, capture_output=True, text=True)
    assert ejecucion.returncode != 0
    assert reporte.read_text() == "reporte anterior"