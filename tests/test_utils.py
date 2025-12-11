import unittest
from unittest.mock import patch, MagicMock
import pathlib
import shutil
import tempfile
import io
import sys
import os
from spa_text_utils.utils import asegurar_directorio, descargar_archivo, ayuda_spa_text_utils
from urllib.error import URLError, HTTPError

class TestUtils(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for file operations
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_asegurar_directorio_creates_dir(self):
        target_dir = os.path.join(self.test_dir, 'new_dir')
        asegurar_directorio(target_dir)
        self.assertTrue(os.path.isdir(target_dir))

    def test_asegurar_directorio_existing_dir(self):
        target_dir = os.path.join(self.test_dir, 'existing_dir')
        os.makedirs(target_dir)
        # Should not raise exception
        asegurar_directorio(target_dir)
        self.assertTrue(os.path.isdir(target_dir))

    @patch('urllib.request.urlretrieve')
    def test_descargar_archivo_success(self, mock_urlretrieve):
        url = 'http://example.com/data.csv'
        filename = 'data.csv'
        subfolder = 'downloads'
        
        # We need to change cwd to temp dir to test the default behavior relative to cwd
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            result = descargar_archivo(url, filename, subfolder)
            
            expected_path = os.path.join(self.test_dir, subfolder, filename)
            # Resolve symlinks for comparison (e.g. /var vs /private/var on macOS)
            self.assertEqual(os.path.realpath(result), os.path.realpath(expected_path))
            self.assertTrue(os.path.isdir(subfolder))
            mock_urlretrieve.assert_called_once()
        finally:
            os.chdir(original_cwd)

    @patch('urllib.request.urlretrieve')
    def test_descargar_archivo_http_error(self, mock_urlretrieve):
        mock_urlretrieve.side_effect = HTTPError(url='http://example.com', code=404, msg='Not Found', hdrs={}, fp=None)
        
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            result = descargar_archivo('http://example.com', 'test.txt')
            self.assertIsNone(result)
        finally:
            os.chdir(original_cwd)

    @patch('urllib.request.urlretrieve')
    def test_descargar_archivo_url_error(self, mock_urlretrieve):
        mock_urlretrieve.side_effect = URLError(reason='Network unreachable')
        
        original_cwd = os.getcwd()
        try:
            os.chdir(self.test_dir)
            result = descargar_archivo('http://example.com', 'test.txt')
            self.assertIsNone(result)
        finally:
            os.chdir(original_cwd)

    def test_ayuda_spa_text_utils(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            ayuda_spa_text_utils()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Documentación de spa_text_utils", output)
        self.assertIn("asegurar_directorio", output)
        self.assertIn("descargar_archivo", output)
        self.assertIn("limpiar_cabeceras_string", output)
        self.assertIn("convertir_a_float_es", output)
        self.assertIn("convertir_a_fecha_es", output)
        self.assertIn("limpiar_celda_texto", output)
        self.assertIn("cargar_csv_es", output)
        self.assertIn("procesar_csv_es", output)



if __name__ == '__main__':
    unittest.main()
