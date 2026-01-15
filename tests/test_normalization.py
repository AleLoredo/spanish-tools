import unittest
from spanish_tools.normalization import clean_header

class TestNormalization(unittest.TestCase):

    def test_clean_header_basic(self):
        self.assertEqual(clean_header("Hola Mundo"), "hola_mundo")

    def test_clean_header_accents(self):
        self.assertEqual(clean_header("Año-Región (Sur)"), "ano_region_sur")
        self.assertEqual(clean_header("Camión"), "camion")
        self.assertEqual(clean_header("Pingüino"), "pinguino")

    def test_clean_header_special_chars(self):
        self.assertEqual(clean_header("Fecha/Hora"), "fecha_hora")
        self.assertEqual(clean_header("¿Pregunta?"), "pregunta")
        self.assertEqual(clean_header("Item #1"), "item_1")
        self.assertEqual(clean_header("100%"), "100")

    def test_clean_header_underscores(self):
        self.assertEqual(clean_header("  Hola   Mundo  "), "hola_mundo")
        self.assertEqual(clean_header("__Hola__Mundo__"), "hola_mundo")
        self.assertEqual(clean_header("Hola - Mundo"), "hola_mundo")

    def test_clean_header_empty(self):
        self.assertEqual(clean_header(""), "")

if __name__ == '__main__':
    unittest.main()
