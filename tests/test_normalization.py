import unittest
from spa_text_utils.normalization import limpiar_cabeceras_string, convertir_a_float_es, convertir_a_fecha_es

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
        self.assertEqual(limpiar_cabeceras_string("   "), "")
        self.assertEqual(limpiar_cabeceras_string("---"), "")

    def test_convertir_a_float_es_numeric(self):
        self.assertEqual(convertir_a_float_es(10), 10.0)
        self.assertEqual(convertir_a_float_es(10.5), 10.5)

    def test_convertir_a_float_es_string(self):
        self.assertEqual(convertir_a_float_es("10,5"), 10.5)
        self.assertEqual(convertir_a_float_es("1.000,50"), 1000.5)
        self.assertEqual(convertir_a_float_es("  -1.234,56 "), -1234.56)

    def test_convertir_a_float_es_invalid(self):
        self.assertIsNone(convertir_a_float_es("abc"))
        self.assertIsNone(convertir_a_float_es("10,5,5")) # Invalid format (two decimals)
        self.assertIsNone(convertir_a_float_es(None))
        self.assertIsNone(convertir_a_float_es([]))
        
        # Ambiguous but valid according to logic (dots are stripped)
        self.assertEqual(convertir_a_float_es("10.5.5"), 1055.0)

    def test_convertir_a_fecha_es_valid(self):
        from datetime import datetime
        self.assertEqual(convertir_a_fecha_es("15/05/2024"), datetime(2024, 5, 15))
        self.assertEqual(convertir_a_fecha_es("01/01/2000"), datetime(2000, 1, 1))
        
    def test_convertir_a_fecha_es_format(self):
        from datetime import datetime
        self.assertEqual(convertir_a_fecha_es("2024-05-15", formato="%Y-%m-%d"), datetime(2024, 5, 15))

    def test_convertir_a_fecha_es_invalid(self):
        self.assertIsNone(convertir_a_fecha_es("invalid"))
        self.assertIsNone(convertir_a_fecha_es("32/01/2024")) # Invalid day
        self.assertIsNone(convertir_a_fecha_es(None))
        self.assertIsNone(convertir_a_fecha_es(123))

if __name__ == '__main__':
    unittest.main()
