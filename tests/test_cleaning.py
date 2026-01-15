import unittest
from spanish_tools.cleaning import clean_string

class TestCleaning(unittest.TestCase):

    def test_clean_string_basic(self):
        self.assertEqual(clean_string("  Hola Mundo  "), "hola mundo")
        self.assertEqual(clean_string("MÁLAGA"), "malaga")

    def test_clean_string_accents(self):
        # Default behavior: remove accents
        self.assertEqual(clean_string("Camión"), "camion")
        self.assertEqual(clean_string("Pingüino"), "pinguino")
        
        # Keep accents
        self.assertEqual(clean_string("Camión", remove_accents=False), "camión")
        self.assertEqual(clean_string("Pingüino", remove_accents=False), "pingüino")

    def test_clean_string_punctuation(self):
        self.assertEqual(clean_string("Hola, mundo!"), "hola mundo")
        self.assertEqual(clean_string("(100%)"), "100")
        self.assertEqual(clean_string("¿Qué tal?"), "que tal")

    def test_clean_string_whitespace(self):
        self.assertEqual(clean_string("  A   B  C  "), "a b c")
        self.assertEqual(clean_string("\tTab\nNewline"), "tab newline")

    def test_clean_string_non_string(self):
        self.assertEqual(clean_string(123), 123)
        self.assertIsNone(clean_string(None))

if __name__ == '__main__':
    unittest.main()
