import pandas as pd
import pytest

from data_profiler import DataProfiler

@pytest.fixture(scope = "module")
def dataframe_test():
    df = pd.DataFrame({"a": [1, 2, 1, pd.NA, 3, 4, 5, 6], 
                       "b": [1, 3, 1, "z", 5, 6, 7, 8], 
                       "c": [1, 4, 1, 7, 2, 3, 4, 5], 
                       "d": [10, 11, 10, 9, 12, 8, -50, 100]
                       })
    return df

@pytest.fixture(scope = "module")
def profiler(dataframe_test):
    profiler = DataProfiler(dataframe_test)
    return profiler

def test_reporte_nulos(profiler):
    serie_nulos = profiler.reporte_nulos()
    total_nulos = sum(value for label, value in serie_nulos.items())
    assert total_nulos == 1

def test_no_muta_original_nulos(profiler, dataframe_test):
    dataframe_test_copy = dataframe_test.copy()
    profiler.reporte_nulos()
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_duplicados(profiler, dataframe_test):
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_duplicados()
    assert resultado == {"total": 2, "filas": [0, 2]}
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_tipos_inconsistentes(profiler, dataframe_test):
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_tipos_inconsistentes()
    assert resultado == {"a": 1, "b": 2, "c": 1, "d": 1}
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_reporte_outliers(profiler, dataframe_test):
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.reporte_outliers()
    assert resultado["total"] == 2
    pd.testing.assert_series_equal(resultado["valores"]["c"], pd.Series([], name = "c", dtype = "int64"))
    pd.testing.assert_series_equal(resultado["valores"]["d"], pd.Series([-50, 100], name = "d", index = [6, 7]))
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)

def test_generar_reporte(profiler, dataframe_test):
    dataframe_test_copy = dataframe_test.copy()
    resultado = profiler.generar_reporte()
    assert str(profiler.reporte_nulos())  in resultado
    assert f"**- Cantidad de filas duplicadas:** {profiler.reporte_duplicados()["total"]}" in resultado
    resultado_inconsistentes = profiler.reporte_tipos_inconsistentes().items()
    inconsistentes = pd.Series({col: cantidad for col, cantidad in resultado_inconsistentes if cantidad > 1})
    assert str(inconsistentes) in resultado
    assert f"**- Total de outliers:** {profiler.reporte_outliers()["total"]}" in resultado
    pd.testing.assert_frame_equal(dataframe_test, dataframe_test_copy)