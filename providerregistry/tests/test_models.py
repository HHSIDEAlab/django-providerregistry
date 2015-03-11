""" test_models.py 
    use mopdel_mommy to test models
"""
#from model_mommy import mommy

from django.test import TestCase
from ..models import NameAlias

class NameAliasModel_TestCase(TestCase):
    def create_NameAlias(self, name="steve", alias="steven"):
        return NameAlias.objects.create(name=name,alias=alias)

    def test_name_alias_creation(self):
        na = self.create_NameAlias()
        self.assertTrue(isinstance(na, NameAlias))
        self.assertEqual(na.__unicode__(), na.name)

    #def test_name_alias_creation_mommy(self):
        #na = mommy.make(NameAlias)
        #self.assertTrue(isinstance(na, NameAlias))
        #self.assertEqual(na.__unicode__(), na.name)
        
