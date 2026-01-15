# Spanish Tools

[![PyPI version](https://img.shields.io/pypi/v/spanish-tools?color=blue)](https://pypi.org/project/spanish-tools/)
[![Python Version](https://img.shields.io/pypi/pyversions/spanish-tools)](https://pypi.org/project/spanish-tools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Spanish Tools** is a Python library specifically designed to simplify the analysis and processing of Spanish language data. It efficiently handles common issues such as encoding, regional numeric formats (decimal comma), dates, and text normalization (accents, 'ñ').

## 🚀 Installation

### Standard Installation (PyPI)
```bash
pip install spanish_tools
```

### Installation in Google Colab
To install the latest development version directly from GitHub:
```python
!pip install git+https://github.com/AleLoredo/spanish-tools.git
```
> **Note:** If you are using the CSV loading functions (`spanish_tools.core`), ensure `pandas` is installed (included by default in Colab and Anaconda).

## ⚡ Quick Start

"Pandas-style" loading and cleaning in two simple steps:

```python
import spanish_tools as spa

# 1. Load Data (Safe)
# Loads Spanish CSV (separador ';') and cleans column names.
df = spa.read_csv("sales_2024.csv")

# 2. Clean Text (Explicit)
# Cleans the content of specific columns (or use fields="all")
df = spa.clean_text(df, fields=["Comments", "City"])

print(df.head())
# Columns: 'sale_date', 'city'
# Content: 'madrid' (clean text)
```

## ✨ Key Features

*   **"Pandas-Native" UX**: Intuitive functions (`read_csv`, `clean_text`) that integrate naturally into your workflow.
*   **Text Normalization**: Robust tools to remove accents, handle 'ñ', and standardize casing.
*   **Header Cleaning**: Converts "dirty" column names (with spaces, accents, symbols) into clean, programmable `snake_case`.

## 📚 API Reference

### 1. Loading and Processing (`spanish_tools.core`)

#### `spa.read_csv`
Localized wrapper for `pandas.read_csv` that loads the file and cleans its headers.

```python
def read_csv(
    ruta_archivo: str,
    separador: str = ';',
    **kwargs
) -> Optional[pd.DataFrame]
```

#### Useful Pandas Arguments (`**kwargs`)
You can customize the loading by passing any of these common arguments:

| Argument | Description | Example |
| :--- | :--- | :--- |
| `encoding` | Fixes strange characters (broken accents). | `encoding='latin1'` (Old Excel) |
| `parse_dates` | Automatically converts columns to datetime. | `parse_dates=['date']` |
| `dayfirst` | **Crucial in Spanish.** Interprets `01/02` as Feb 1st. | `dayfirst=True` |
| `dtype` | Forces data type (e.g., preserve leading zeros in IDs). | `dtype={'dni': str}` |
| `skiprows` | Skips initial lines (titles, logos). | `skiprows=3` |
| `na_values` | Defines what text counts as "null data". | `na_values=['-', 'N/A']` |

---

#### `spa.clean_text`
Cleans the text content of a loaded DataFrame.

```python
def clean_text(
    df: pd.DataFrame, 
    fields: List[str] | str,
    quitar_acentos: bool = True
) -> pd.DataFrame
```
*   **fields**: Columns to clean. Can be a list of names `['col_a']` or `"all"` for the entire DataFrame.

### 2. Normalization

#### `limpiar_cabeceras_string`
Converts text to `snake_case` format, ideal for variable or column names.

```python
import spanish_tools as spa

print(spa.limpiar_cabeceras_string("Creation Year (2024)"))
# Output: "creation_year_2024"
```

### 3. Text Cleaning

#### `limpiar_celda_texto`
Atomic cleaning for a text string. Removes unnecessary punctuation, extra spaces, and optionally accents.

```python
import spanish_tools as spa

text = "  HELLO   WORLD! "
print(spa.limpiar_celda_texto(text))
# Output: "hello world"
```

## 🤝 Contributing
Contributions are welcome! If you find a bug or have an idea for a new feature:
1.  Fork the repository.
2.  Create a branch for your feature (`git checkout -b feature/new-feature`).
3.  Commit your changes (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature/new-feature`).
5.  Open a Pull Request.

## 📄 License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
