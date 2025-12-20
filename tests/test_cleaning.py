import unittest
from spanish_tools.cleaning import limpiar_celda_texto

class TestCleaning(unittest.TestCase):

    def test_limpiar_celda_texto_basic(self):
        self.assertEqual(limpiar_celda_texto("  Hola Mundo  "), "hola mundo")
        self.assertEqual(limpiar_celda_texto("MÁLAGA"), "malaga")

    def test_limpiar_celda_texto_accents(self):
        # Default behavior: remove accents
        self.assertEqual(limpiar_celda_texto("Camión"), "camion")
        self.assertEqual(limpiar_celda_texto("Pingüino"), "pinguino")
        
        # Keep accents
        self.assertEqual(limpiar_celda_texto("Camión", quitar_acentos=False), "camión")
        self.assertEqual(limpiar_celda_texto("Pingüino", quitar_acentos=False), "pingüino")

    def test_limpiar_celda_texto_punctuation(self):
        self.assertEqual(limpiar_celda_texto("Hola, mundo!"), "hola mundo")
        self.assertEqual(limpiar_celda_texto("(100%)"), "100")
        self.assertEqual(limpiar_celda_texto("¿Qué tal?"), "que tal")

    def test_limpiar_celda_texto_whitespace(self):
        self.assertEqual(limpiar_celda_texto("  A   B  C  "), "a b c")
        self.assertEqual(limpiar_celda_texto("\tTab\nNewline"), "tab newline")

    def test_limpiar_celda_texto_non_string(self):
        self.assertEqual(limpiar_celda_texto(123), 123)
        self.assertIsNone(limpiar_celda_texto(None))

if __name__ == '__main__':
    unittest.main()
