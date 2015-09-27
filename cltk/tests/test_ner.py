"""Test cltk.ner."""

__author__ = 'Kyle P. Johnson <kyle@kyle-p-johnson.com>'
__license__ = 'MIT License. See LICENSE.'

from cltk.ner import ner
from cltk.stem.latin.j_v import JVReplacer
import os
import unittest


class TestSequenceFunctions(unittest.TestCase):  # pylint: disable=R0904
    """Class for unittest"""
    def test_check_latest_latin(self):
        """Test _check_latest_data()"""
        ner._check_latest_data('latin')
        names_path = os.path.expanduser('~/cltk_data/latin/model/latin_models_cltk/ner/proper_names.txt')
        self.assertTrue(os.path.isfile(names_path))

    def test_make_ner_str_list_latin(self):
        """Test make_ner()."""
        jv_replacer = JVReplacer()
        text_str = """ut Venus, ut Sirius, ut Spica, ut aliae quae primae dicuntur esse mangitudinis."""
        jv_replacer = JVReplacer()
        text_str_iu = jv_replacer.replace(text_str)
        tokens = ner.make_ner('latin', input_text=text_str_iu, output_type=list)
        target = [('ut',), ('Uenus',), (',',), ('ut',), ('Sirius', 'Entity'), (',',), ('ut',), ('Spica', 'Entity'), (',',), ('ut',), ('aliae',), ('quae',), ('primae',), ('dicuntur',), ('esse',), ('mangitudinis',), ('.',)]
        self.assertEqual(tokens, target)

    def test_make_ner_list_list_latin(self):
        """Test make_ner()."""
        text_list = ['ut', 'Venus', 'Sirius']
        jv_replacer = JVReplacer()
        text_list_iu = [jv_replacer.replace(x) for x in text_list]
        tokens = ner.make_ner('latin', input_text=text_list_iu, output_type=list)
        target = [('ut',), ('Uenus',), ('Sirius', 'Entity')]
        self.assertEqual(tokens, target)

if __name__ == '__main__':
    unittest.main()
