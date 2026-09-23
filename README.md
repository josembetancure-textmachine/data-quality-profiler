# Data Quality Profiler

> **English summary:** A small Python tool that profiles the quality of a tabular dataset (CSV, Excel, or an in-memory DataFrame): it reports missing values, duplicate rows, inconsistent data types per column, and statistical outliers (IQR method), then compiles everything into a single readable Markdown report. Built as the second step of a self-directed transition from philology into data analysis and NLP — the first serious exercise in applying object-oriented design to a real data problem.
>
> Testing this tool against real messy data surfaced a genuine, non-obvious limitation: when loading from `.csv`, a numeric column contaminated with a single text value gets silently read as text in its entirety, hiding the inconsistency from both the type-checker and the outlier-checker. That limitation — why it happens, why it doesn't affect `.xlsx` or an in-memory DataFrame, and why it's documented instead of silently "fixed" — is explained below and in `NOTAS_DATA_QUALITY_PROFILER.md`.
>
> *(The rest of this document is in Spanish.)*

Herramienta en Python que perfila la calidad de un dataset tabular (CSV, Excel o un DataFrame en memoria): reporta valores nulos, filas duplicadas, tipos de datos inconsistentes por columna y outliers estadísticos (método IQR), y compila todo en un único reporte legible en Markdown.

## Contexto

Este proyecto se realiza como segundo hito de un plan de transición al sector tecnológico que desemboca en el procesamiento del lenguaje natural. Es el primer contacto serio con Programación Orientada a Objetos aplicada a un problema real de análisis de datos: en vez de un script de un solo uso, una herramienta reutilizable que se puede aplicar a cualquier dataset tabular.

## Instalación

Requisitos previos: Python 3.12 o superior.

```bash
git clone https://github.com/josembetancure-textmachine/data-quality-profiler.git
cd data-quality-profiler
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows, el paso de activación del entorno virtual cambia a `.venv\Scripts\activate`.

## Uso

Como herramienta de línea de comandos:

```bash
python3 data_profiler.py archivo_a_analizar.csv
```

Esto genera `ejemplo_reporte.md` en el directorio actual, con el reporte completo.

También puede usarse importando la clase directamente:

```python
from data_profiler import DataProfiler

perfil = DataProfiler("mi_dataset.csv")  # o .xlsx, o un pandas.DataFrame ya construido
print(perfil.generar_reporte())

# O consultar cada método por separado:
perfil.reporte_nulos()
perfil.reporte_duplicados()
perfil.reporte_tipos_inconsistentes()
perfil.reporte_outliers()
```

### Fuente del dataset de prueba

E.S.E. Hospital Universitario Hernando Moncaleano Perdomo, Neiva, Huila. [ENFERMEDADES — Datos Abiertos Colombia](https://www.datos.gov.co/Salud-y-Protecci-n-Social/ENFERMEDADES/5r4m-umt6). Consultado: 22 de septiembre de 2026. Licencia CC BY-SA 4.0.

## Estructura del proyecto

```
data-quality-profiler/
├── data_profiler.py                      [Clase DataProfiler y CLI]
├── tests/
│   └── test_data_profiler.py             [Suite de pytest]
├── conftest.py                           [Existe para que pytest encuentre data_profiler.py al importar desde tests/]
├── ejemplo_reporte.md                    [Ejemplo de reporte generado sobre un dataset real]
├── NOTAS_DATA_QUALITY_PROFILER.md        [Proceso de pensamiento y decisiones de diseño. Sirve para los reclutadores.]
├── requirements.txt
└── .gitignore
```

## Decisiones de diseño

- **IQR (rango intercuartílico) para detectar outliers**, con el multiplicador estándar de 1.5 (outliers leves, no extremos). Es un método simple, no paramétrico, y suficiente para este nivel del proyecto — no requiere asumir una distribución normal de los datos.
- **Offset de `+2` en los índices de filas duplicadas** cuando el origen es un archivo (`.csv`/`.xlsx`), para que el número de fila reportado corresponda a la fila real del archivo (encabezado + índice base 1 de una hoja de cálculo), no al índice interno de pandas. Cuando el origen es un DataFrame en memoria, se reporta el índice tal cual, sin ajustar.
- **`self.source` conserva la ruta o el string `"DataFrame en memoria"`**, para que tanto `__repr__` como `generar_reporte()` puedan indicar de dónde vinieron los datos analizados.

## Limitaciones conocidas

**Los datos provenientes de `.csv` con una columna numérica contaminada por un solo valor de texto no se detectan como inconsistentes, y esa columna queda excluida silenciosamente del chequeo de outliers.**

Esto ocurre porque `.csv` es texto plano sin información de tipo por celda: si una columna contiene `[25, 30, "treinta"]`, pandas no puede decidir un tipo numérico único para toda la columna y la lee entera como texto (`str`). Como `reporte_tipos_inconsistentes()` cuenta tipos de Python después de descartar nulos, toda la columna aparece como un solo tipo (`str`) — la inconsistencia real (un valor no numérico entre datos numéricos) no se refleja. Por la misma razón, `reporte_outliers()` filtra solo columnas que pandas reconoce como numéricas (`select_dtypes(include="number")`), así que esta columna queda fuera del chequeo sin ningún aviso.

**Esta limitación es específica de `.csv` — no aplica a `.xlsx` ni a un `pandas.DataFrame` construido directamente en Python.** Excel almacena el tipo de cada celda individualmente, así que `pd.read_excel()` reconstruye la mezcla real de tipos (`[25, 30, "treinta"]` se lee como tres valores de tipos distintos, tal como se construyeron), y lo mismo ocurre al pasar un DataFrame ya construido en memoria. En ambos casos, `reporte_tipos_inconsistentes()` sí detecta la mezcla correctamente.

Se documenta como límite conocido del proyecto en su alcance actual, no como error silencioso sin registrar.

## Autoría

Para conocer el proceso de desarrollo completo, las decisiones de diseño y la postura sobre el uso de IA en este proyecto, ver [NOTAS_DATA_QUALITY_PROFILER.md](NOTAS_DATA_QUALITY_PROFILER.md).