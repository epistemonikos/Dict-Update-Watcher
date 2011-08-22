# -*- coding: utf-8 -*-
import unittest

from dict_update_watcher import DictUpdateWatcher


class TestDictUpdateWatcher(unittest.TestCase):
    def setUp(self):
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

    def test_select_field(self):
        self.assertEqual('primary-study', self.document.get('info.classification'))
    
    def test_get_inexistence_field(self):
        self.assertEqual(None, self.document.get('info.no_existe'))
    
    def test_list(self):
        for i in range(0, len(self.document.info.author)):
            self.assertEqual(self.dict["info"]["author"][i], self.document.info.author[i])




if __name__ == '__main__':
    unittest.main()