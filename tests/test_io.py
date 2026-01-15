import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from spanish_tools.io import procesar_csv_es

try:
    import pandas as pd
    PANDAS_INSTALLED = True
except ImportError:
    PANDAS_INSTALLED = False

class TestIO(unittest.TestCase):

    def test_procesar_csv_es_success(self):
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.columns = ['Columna 1', 'Columna 2']
        mock_pd.read_csv.return_value = mock_df
        
        # Mock apply for text cleaning
        # The code does: df[col] = df[col].astype(str).apply(...)
        mock_series = MagicMock()
        mock_df.__getitem__.return_value = mock_series
        
        # Mock .astype(str) to return the same series (or a mock that has .apply)
        mock_series.astype.return_value = mock_series
        mock_series.apply.return_value = mock_series

        with patch.dict('sys.modules', {'pandas': mock_pd}):
            df = procesar_csv_es('datos.csv', columnas_texto_a_limpiar=['Columna 1'])
            
            self.assertEqual(df, mock_df)
            
            # Verify rename was called (header cleaning)
            mock_df.rename.assert_called_once()
            args, kwargs = mock_df.rename.call_args
            self.assertIn('columns', kwargs)
            
            # Verify text cleaning was applied
            mock_df.__getitem__.assert_called()
            mock_series.astype.assert_called_with(str)
            mock_series.apply.assert_called()

    def test_procesar_csv_es_load_error(self):
        mock_pd = MagicMock()
        mock_pd.read_csv.side_effect = FileNotFoundError()
        
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            result = procesar_csv_es('no_existe.csv')
            self.assertIsNone(result)

    @unittest.skipUnless(PANDAS_INSTALLED, "Pandas not installed")
    def test_integration_real_file(self):
        """
        Integration test using the real 'tests/test.csv' file.
        """
        # Construct path to tests/test.csv
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'test.csv')
        
        # Verify file exists
        if not os.path.exists(csv_path):
            self.skipTest(f"Test file not found: {csv_path}")

        # Process the CSV
        # The file uses comma separator based on inspection
        df = procesar_csv_es(
            csv_path, 
            columnas_texto_a_limpiar=['Nombre'], 
            separador=','
        )
        
        self.assertIsNotNone(df)
        
        # Verify header cleaning
        # 'Apellido(s)' -> 'apellido_s'
        self.assertIn('apellido_s', df.columns)
        self.assertIn('nombre', df.columns)
        self.assertIn('direccion_de_correo', df.columns)
        
        # Verify text cleaning in 'Nombre' column
        # "Valentín Darío" -> "valentin dario"
        # We need to find the row where apellido_s is 'Camaño' (or 'cama_o' if headers were cleaned? No, values are not cleaned unless specified)
        # Wait, we didn't clean 'Apellido(s)', only 'Nombre'.
        # But wait, 'Camaño' might be loaded as is.
        
        # Let's check the first row content
        first_row = df.iloc[0]
        # 'Valentín Darío' should be cleaned to 'valentin dario'
        self.assertEqual(first_row['nombre'], 'valentin dario')
        
        # 'Camaño' in 'apellido_s' column should remain as is because we didn't ask to clean it
        # However, pandas might read it with encoding issues if not handled, but we use utf-8 by default.
        # The file content viewed earlier showed "Camaño".
        self.assertEqual(first_row['apellido_s'], 'Camaño')

if __name__ == '__main__':
    unittest.main()
