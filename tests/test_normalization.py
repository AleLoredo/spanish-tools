import unittest
from spanish_tools.normalization import limpiar_cabeceras_string

class TestNormalization(unittest.TestCase):

    def test_limpiar_cabeceras_string_basic(self):
        self.assertEqual(limpiar_cabeceras_string("Hola Mundo"), "hola_mundo")

    def test_limpiar_cabeceras_string_accents(self):
        self.assertEqual(limpiar_cabeceras_string("Año-Región (Sur)"), "ano_region_sur")
        self.assertEqual(limpiar_cabeceras_string("Camión"), "camion")
        self.assertEqual(limpiar_cabeceras_string("Pingüino"), "pinguino")

    def test_limpiar_cabeceras_string_special_chars(self):
        self.assertEqual(limpiar_cabeceras_string("Fecha/Hora"), "fecha_hora")
        self.assertEqual(limpiar_cabeceras_string("¿Pregunta?"), "pregunta")
        self.assertEqual(limpiar_cabeceras_string("Item #1"), "item_1")
        self.assertEqual(limpiar_cabeceras_string("100%"), "100")

    def test_limpiar_cabeceras_string_underscores(self):
        self.assertEqual(limpiar_cabeceras_string("  Hola   Mundo  "), "hola_mundo")
        self.assertEqual(limpiar_cabeceras_string("__Hola__Mundo__"), "hola_mundo")
        self.assertEqual(limpiar_cabeceras_string("Hola - Mundo"), "hola_mundo")

    def test_limpiar_cabeceras_string_empty(self):
        self.assertEqual(limpiar_cabeceras_string(""), "")

if __name__ == '__main__':
    unittest.main()
