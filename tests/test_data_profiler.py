import pandas as pd
import pytest

from data_profiler import DataProfiler

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
    '''Verifica que generar_reporte() incluya los resultados de los cuatro métodos de reporte en el string final, sin modificar el DataFrame original.'''
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.generar_reporte()
    assert str(profiler.reporte_nulos())  in resultado
    assert f"**- Cantidad de filas duplicadas:** {profiler.reporte_duplicados()["total"]}" in resultado
    resultado_inconsistentes = profiler.reporte_tipos_inconsistentes().items()
    inconsistentes = pd.Series({col: cantidad for col, cantidad in resultado_inconsistentes if cantidad > 1})
    assert str(inconsistentes) in resultado
    assert f"**- Total de outliers:** {profiler.reporte_outliers()["total"]}" in resultado
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)