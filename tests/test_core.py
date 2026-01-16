import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from spanish_tools.core import load_data, clean_text

try:
    import pandas as pd
    PANDAS_INSTALLED = True
except ImportError:
    PANDAS_INSTALLED = False

class TestCore(unittest.TestCase):

    def test_load_data_csv_success(self):
        """Test simple CSV load and header cleaning"""
        mock_pd = MagicMock()
        mock_df = MagicMock()
        # Mocking suffix to simulate .csv
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value.suffix.lower.return_value = '.csv'
            mock_path.return_value.name = 'datos.csv'
            
            mock_df.columns = ['Columna 1', 'Columna 2']
            mock_pd.read_csv.return_value = mock_df
            
            with patch.dict('sys.modules', {'pandas': mock_pd}):
                df = load_data('datos.csv')
                
                self.assertEqual(df, mock_df)
                
                # Check header rename
                mock_df.rename.assert_called_once()
                
                # Check pandas.read_csv called
                mock_pd.read_csv.assert_called()
                call_kwargs = mock_pd.read_csv.call_args[1]
                self.assertEqual(call_kwargs['decimal'], ',')
                self.assertEqual(call_kwargs['sep'], ';')

    def test_load_data_clipboard(self):
        """Test clipboard loading"""
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.columns = ['Columna_1']
        mock_pd.read_clipboard.return_value = mock_df
        
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            df = load_data('clipboard')
            
            mock_pd.read_clipboard.assert_called_once()
            # Check cleaning happened
            mock_df.rename.assert_called_once()

    def test_load_data_ods(self):
        """Test ODS loading"""
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.columns = ['Columna_1']
        mock_pd.read_excel.return_value = mock_df
        
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value.suffix.lower.return_value = '.ods'
            mock_path.return_value.name = 'datos.ods'
            
            with patch.dict('sys.modules', {'pandas': mock_pd}):
                df = load_data('datos.ods')
                
                # Check engine='odf' passed to read_excel
                mock_pd.read_excel.assert_called()
                call_kwargs = mock_pd.read_excel.call_args[1]
                self.assertEqual(call_kwargs['engine'], 'odf')

    def test_load_data_xml(self):
        """Test XML loading"""
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.columns = ['Columna_1']
        mock_pd.read_xml.return_value = mock_df
        
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value.suffix.lower.return_value = '.xml'
            mock_path.return_value.name = 'datos.xml'
            
            with patch.dict('sys.modules', {'pandas': mock_pd}):
                df = load_data('datos.xml')
                
                mock_pd.read_xml.assert_called_once()

    def test_clean_text_basic(self):
        """Test text cleaning on specific columns of an existing DF"""
        # Setup a mock DF that allows iteration
        mock_df = MagicMock()
        mock_df.columns = ['col1']
        
        mock_series = MagicMock()
        # Mocking __getitem__ (df['col1'])
        mock_df.__getitem__.return_value = mock_series
        mock_series.astype.return_value = mock_series
        mock_series.apply.return_value = mock_series

        df = clean_text(mock_df, fields=['col1'])
        
        # Verify cleaning
        mock_series.apply.assert_called()

    def test_clean_text_all(self):
        """Test clean_text works with 'all' keyword"""
        mock_df = MagicMock()
        
        # Mock columns to support iteration and tolist
        mock_columns = MagicMock()
        mock_columns.tolist.return_value = ['col1', 'col2']
        mock_columns.__iter__.return_value = iter(['col1', 'col2'])
        mock_df.columns = mock_columns
        
        mock_series = MagicMock()
        mock_df.__getitem__.return_value = mock_series
        mock_series.astype.return_value = mock_series
        mock_series.apply.return_value = mock_series

        clean_text(mock_df, fields='all')
        
        # Should clean 2 columns
        self.assertEqual(mock_series.apply.call_count, 2)

    def test_load_data_file_error(self):
        mock_pd = MagicMock()
        mock_pd.read_csv.side_effect = FileNotFoundError()
        
        with patch.dict('sys.modules', {'pandas': mock_pd}):
            df = load_data('no_existe.csv')
            self.assertIsNone(df)

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
        # 1. READ (Safe)
        df = load_data(
            csv_path, 
            separador=','
        )
        
        self.assertIsNotNone(df)
        self.assertIn('nombre', df.columns) # Cleaned header
        
        # 2. CLEAN TEXT (Explicit)
        df = clean_text(df, fields=['nombre'])
        
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

    def test_load_data_mojibake_header(self):
        """Test that load_data fixes mojibake in headers"""
        # Mock pandas read_csv to return a DF with broken headers
        mock_pd = MagicMock()
        mock_df = MagicMock()
        mock_df.columns = ['AÃ±o', 'RegiÃ³n']
        mock_pd.read_csv.return_value = mock_df
        
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value.suffix.lower.return_value = '.csv'
            mock_path.return_value.name = 'dummy.csv'
            
            with patch.dict('sys.modules', {'pandas': mock_pd}):
                df = load_data('dummy.csv')
                
                # Check what rename was called with
                mock_df.rename.assert_called_once()
                args, kwargs = mock_df.rename.call_args
                rename_map = kwargs['columns']
                
                self.assertEqual(rename_map['AÃ±o'], 'ano')

    @unittest.skipUnless(PANDAS_INSTALLED, "Pandas not installed")
    def test_load_data_mojibake_content_content_real_pandas(self):
        """
        Real pandas test for load_data content fixing.
        """
        mock_pd = MagicMock()
        real_df = pd.DataFrame({'Ciudad': ['CamirÃ±o', 'CÓRDOBA']})
        mock_pd.read_csv.return_value = real_df
        
        with patch('pathlib.Path') as mock_path: # Need to mock Path for load_data extension check
            mock_path.return_value.suffix.lower.return_value = '.csv'
            
            with patch.dict('sys.modules', {'pandas': mock_pd}):
                df = load_data('dummy.csv')
                
                self.assertIn('ciudad', df.columns)
                self.assertEqual(df['ciudad'][0], 'Camirño')
                self.assertEqual(df['ciudad'][1], 'CÓRDOBA')
