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
        self.assertEqual('systematic-review',self.document.info.classification)

    def test_updated_fields(self):
        self.assertEqual([], self.document.updated_fields())
        self.document.info.classification = 'systematic-review'
        self.assertEqual(['info.classification'],self.document.updated_fields())

    def test_updated_fields_three_levels(self):
        self.assertEqual([], self.document.updated_fields())
        self.document.languages.es = {'title': 'title'}
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
        #Testear cuando no tiene dict
        self.assertEqual(self.dict['languages']['en'],self.document.languages.en.get_dict())

    def test_get_keys(self):
        received_keys = self.document.keys()
        received_keys.sort()
        self.assertEqual(['id', 'info', 'languages', 'modified'],received_keys)

    def test_correct_implementation_of_compare(self):
        #TODO revisar
        document2 = DictUpdateWatcher(self.dict)
        self.assertEqual(self.document, document2)
    
    def test_get_dict_recursive(self):
        #Testear cuando no tiene dict
        document2 = DictUpdateWatcher(self.dict)
        self.assertEqual(self.dict, self.document.get_dict(recursive = True))

    def test_inherit_class_changed(self):
        class Example(DictUpdateWatcher):pass
        ex = Example({"daniel": {"saludo": "hola"}})
        ex.daniel.saludo = "chao"
        self.assertEqual(['daniel.saludo'], ex.updated_fields())
        
    def test_get_dict_recursive_not_clear_the_modified_elements(self):
        self.document.info.classification = 'systematic-review'
        self.assertEqual(['info.classification'],self.document.updated_fields())
        self.document.get_dict(True)
        self.assertEqual(['info.classification'],self.document.updated_fields())

        


if __name__ == '__main__':
    unittest.main()