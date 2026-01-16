# Spanish Tools

[![PyPI version](https://img.shields.io/pypi/v/spanish-tools?color=blue)](https://pypi.org/project/spanish-tools/)
[![Python Version](https://img.shields.io/pypi/pyversions/spanish-tools)](https://pypi.org/project/spanish-tools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Spanish Tools** is a Python library specifically designed to simplify the loading of Spanish language datasets for processing purposes. It  aids with fixing encoding issues, regional numeric formats (decimal comma), dates, and text normalization (accents, 'ñ') using just one function. It is built on top of pandas and is compatible with any pandas DataFrame.

## 🚀 Install
```bash
pip install spanish_tools
```
## Import
```python
import spanish_tools as spa
```
## Load Data and apply cleaning automatically
```python
df = spa.load_data("sales_2024.xlsx")
```

For a more detailed walkthrough, continue reading.

## ⚡ Detailed walkthrough

```python
import spanish_tools as spa

# 1. Load Data (Universal: CSV, Excel, etc.)
# This works for .csv, .xls, and .xlsx automatically.
# - Sets Spanish defaults (dec=',', sep=';') for CSVs.
# - Cleans headers to snake_case and removes any spanish special character such as 'ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü'.
# - In case of encoding issues, it applyes an automatic fix to encoding (mojibake) in all text columns.
df = spa.load_data("sales_2024.xlsx")

# You can still pass pandas arguments:
df_csv = spa.load_data(
    "sales_old.csv", 
    encoding="latin1", 
    parse_dates=["fecha"]
)

# 2. Clean Text (Explicit)
# This will clean the content of specific columns (removes accents, standardizes spaces, lowercases)
df = spa.clean_text(df, fields=["comments", "city"])

# 3. Clean Text (All)
# Or clean the entire DataFrame
df = spa.clean_text(df, fields="all", remove_accents=True)

print(df.head())
# Columns: 'fecha', 'ciudad' (snake_case headers)
# Content: 'malaga' (clean text)
```

## ✨ Key Features

*   **Universal Loader**: `load_data` handles CSV and Excel files seamlessly.
*   **Auto-Cleaning**: Automatically fixes mojibake (encoding errors) and normalizes headers upon loading.
*   **"Pandas-Native" UX**: Intuitive functions that integrate naturally into your workflow.

## 📚 API Reference

### 1. Loading and Processing (`spanish_tools.core`)

#### `spa.load_data`
Universal loader for CSV, Excel, ODS, XML, and Clipboard. Wraps `pandas` and applies automatic Spanish-focused cleaning.

```python
def load_data(
    ruta_archivo: str,
    separador: str = ';',
    **kwargs
) -> Optional[pd.DataFrame]
```

#### Supported Formats:
*   **CSV** (`.csv`): Auto-configured for Spanish standards (`;`, `,`).
*   **Excel** (`.xls`, `.xlsx`): Standard Excel files.
*   **OpenDocument** (`.ods`): Common in Public Administration.
*   **XML** (`.xml`): Generic XML parsing.
*   **Clipboard**: Use `spa.load_data("clipboard")` to load copied data.

#### Useful Pandas Arguments (`**kwargs`)
You can customize the loading by passing any standard pandas arguments:

| Argument | Description | Example |
| :--- | :--- | :--- |
| `sheet_name` | (Excel/ODS) specific sheet to load. | `sheet_name='DataV1'` |
| `encoding` | (CSV) Fixes strange characters. | `encoding='latin1'` |
| `parse_dates` | Automatically converts columns to datetime. | `parse_dates=['date']` |
| `dtype` | Forces data type. | `dtype={'dni': str}` |

---

#### `spa.clean_text`
Cleans the text content of a loaded DataFrame.

```python
def clean_text(
    df: pd.DataFrame, 
    fields: List[str] | str,
    remove_accents: bool = True,
    **kwargs
) -> pd.DataFrame
```
*   **fields**: Columns to clean. Can be a list of names `['col_a']` or `"all"` for the entire DataFrame.
*   **remove_accents**: If `True` (default), removes accents ('á' -> 'a') and normalizes 'ñ'.
*   **kwargs**: Included for potential future extensions, currently ignored.

### 2. Normalization

#### `clean_header`
Converts text to `snake_case` format, ideal for variable or column names.

```python
import spanish_tools as spa

print(spa.clean_header("Creation Year (2024)"))
# Output: "creation_year_2024"
```

### 3. Text Cleaning

#### `clean_string`
Atomic cleaning for a text string. Removes unnecessary punctuation, extra spaces, and optionally accents.

```python
import spanish_tools as spa

text = "  HELLO   WORLD! "
print(spa.clean_string(text))
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
