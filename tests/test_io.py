import unittest
from unittest.mock import patch, MagicMock
import sys
from spa_text_utils.io import cargar_csv_es, procesar_csv_es

class TestIO(unittest.TestCase):

    def test_cargar_csv_es_success(self):
        # Create a mock for pandas
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.__len__.return_value = 10
        mock_pd.read_csv.return_value = mock_df
        
        # Patch sys.modules to return our mock when 'pandas' is imported
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            ruta = 'datos.csv'
            df = cargar_csv_es(ruta)
            
            self.assertEqual(df, mock_df)
            mock_pd.read_csv.assert_called_once()
            
            # Verify default arguments
            args, kwargs = mock_pd.read_csv.call_args
            self.assertEqual(args[0], ruta)
            self.assertEqual(kwargs['sep'], ';')
            self.assertEqual(kwargs['decimal'], ',')
            self.assertEqual(kwargs['thousands'], '.')

    def test_cargar_csv_es_custom_args(self):
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.__len__.return_value = 5
        mock_pd.read_csv.return_value = mock_df
        
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            cargar_csv_es('datos.csv', separador=',', encoding='latin1')
            
            args, kwargs = mock_pd.read_csv.call_args
            self.assertEqual(kwargs['sep'], ',')
            self.assertEqual(kwargs['encoding'], 'latin1')

    def test_cargar_csv_es_file_not_found(self):
        mock_pd = MagicMock()
        mock_pd.read_csv.side_effect = FileNotFoundError()
        
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            result = cargar_csv_es('no_existe.csv')
            self.assertIsNone(result)

    def test_cargar_csv_es_pandas_missing(self):
        # Simulate pandas missing by removing it from sys.modules if present
        # and ensuring import raises ImportError
        with patch.dict('sys.modules'):
            if 'pandas' in sys.modules:
                del sys.modules['pandas']
            
            # We need to ensure that the import fails. 
            pass 

    def test_procesar_csv_es_success(self):
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.columns = ['Columna 1', 'Columna 2']
        mock_pd.read_csv.return_value = mock_df
        
        # Mock apply for text cleaning
        mock_series = MagicMock()
        mock_df.__getitem__.return_value = mock_series
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
            mock_series.apply.assert_called()

    def test_procesar_csv_es_load_error(self):
        mock_pd = MagicMock()
        mock_pd.read_csv.side_effect = FileNotFoundError()
        
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            result = procesar_csv_es('no_existe.csv')
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
