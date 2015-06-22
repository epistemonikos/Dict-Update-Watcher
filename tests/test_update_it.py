# -*- coding: utf-8 -*-
import unittest

from dict_update_watcher import DictUpdateWatcher


class TestDictUpdateWatcher(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dict = {
            "info":
            {
                "doi": "10.1056/NEJM199803263381303",
                "classification": "primary-study",
                "author": [
                    "SE. Inzucchi",
                    "DG. Maggs",
                    "GR. Spollett",
                    "SL. Page",
                    "FS. Rife",
                    "V. Walton",
                    "GI. Shulman"
                ],
                "strategy": None,
                "source": "PubMed",
                "same_as": None,
                "pubmed": "9516221",
                "date": None,
                "type": "http://purl.org/ontology/bibo/Document"
            },
            "languages": {
                "en": {
                    "title": "Efficacy and Metabolic Effects of Metformin and Troglitazone in Type II Diabetes Mellitus"
                }
            },
            "modified": 1308190099,
            "id": "123"
        }
        self.document = DictUpdateWatcher(self.dict)

    def test_load_from_json(self):
        self.assertEqual(self.dict['info']['classification'], self.document.info.classification)

    def test_update_document(self):
        self.document.info.classification = 'systematic-review'
        self.assertEqual('systematic-review', self.document.info.classification)

    def test_updated_fields(self):
        self.assertEqual([], self.document.updated_fields())
        self.document.info.classification = 'systematic-review'
        self.assertEqual(['info.classification'], self.document.updated_fields())

    def test_updated_fields_three_levels(self):
        self.assertEqual([], self.document.updated_fields())
        self.document.languages.es = DictUpdateWatcher({'title': 'title'})
        self.document.languages.es.copyright = 'copyright'
        self.document.languages.en.copyright = 'systematic-review'
        self.assertEqual(['languages.es', 'languages.en.copyright'], self.document.updated_fields())

    def test_select_field(self):
        self.assertEqual('primary-study', self.document.get('info.classification'))

    def test_get_inexistence_field(self):
        self.assertEqual(None, self.document.get('info.no_existe'))

    def test_get_default_value(self):
        self.assertEqual('default_value', self.document.get('info.no_existe', 'default_value'))

    def test_list(self):
        for i in range(0, len(self.document.info.author)):
            self.assertEqual(self.dict["info"]["author"][i], self.document.info.author[i])

    def test_get_dict(self):
        # Testear cuando no tiene dict
        self.assertEqual(self.dict['languages']['en'], self.document.languages.en.get_dict())

    def test_get_keys(self):
        received_keys = self.document.keys()
        received_keys.sort()
        self.assertEqual(['id', 'info', 'languages', 'modified'], received_keys)

    def test_correct_implementation_of_compare(self):
        # TODO revisar
        document2 = DictUpdateWatcher(self.dict)
        self.assertEqual(self.document, document2)

    def test_get_dict_recursive(self):
        # Testear cuando no tiene dict
        document2 = DictUpdateWatcher(self.dict)
        self.assertEqual(self.dict, self.document.get_dict(recursive=True))

    def test_inherit_class_changed(self):
        class Example(DictUpdateWatcher):
            pass
        ex = Example({"daniel": {"saludo": "hola"}})
        ex.daniel.saludo = "chao"
        self.assertEqual(['daniel.saludo'], ex.updated_fields())

    def test_get_dict_recursive_not_clear_the_modified_elements(self):
        self.document.info.classification = 'systematic-review'
        self.assertEqual(['info.classification'], self.document.updated_fields())
        self.document.get_dict(True)
        self.assertEqual(['info.classification'], self.document.updated_fields())

    def test_inherit_class_changed_including_base(self):
        class Example(DictUpdateWatcher):
            def __init__(self, dict_):
                super(Example, self).__init__(dict_)
        ex = Example(self.dict)
        ex.daniel = "chao"
        ex.languages.es = 'es'
        ex.languages.en.nuevo = 'nuevo'
        ex.relations = 'relations'
        received_update = ex.updated_fields()
        received_update.sort()
        self.assertEqual(['daniel', 'languages.en.nuevo', 'languages.es', 'relations'], received_update)

    def test_inherit_class_changed_with_ommit_elements(self):
        class Example(DictUpdateWatcher):
            def __init__(self, dict_):
                super(Example, self).__init__(dict_)
                self._ommit = ['languages.en', 'daniel']
        ex = Example(self.dict)
        ex.daniel = "chao"
        ex.languages.es = 'es'
        ex.languages.en.nuevo = 'nuevo'
        ex.relations = 'relations'
        received_update = ex.updated_fields()
        received_update.sort()
        self.assertEqual(['languages.es', 'relations'], received_update)

    def test_set_dict_inline(self):
        self.document.set('info.classification', 'overview')
        self.assertEqual('overview', self.document.info.classification)

    def test_set_dict_with_unexistent_elements(self):
        self.document.set('otra.saludo', 'hola')
        self.assertEqual('hola', self.document.otra.saludo)

    def test_set_dict_one_element(self):
        self.document.set('saludo', 'hola')
        self.assertEqual('hola', self.document.saludo)

    def test_get_element_empty_with_default_value(self):
        self.document.set('probando', None)
        self.assertEqual({}, self.document.get('probando', {}))

    def test_delete_field(self):
        del self.document.info.classification
        self.assertIn('info.classification', self.document.updated_fields())
        self.assertIsNone(self.document.get('info.classification'))

    def test_delete_field_like_dict(self):
        self.document.info.unset('classification')
        self.assertIn('info.classification', self.document.updated_fields())
        self.assertIsNone(self.document.get('info.classification'))


if __name__ == '__main__':
    unittest.main()
