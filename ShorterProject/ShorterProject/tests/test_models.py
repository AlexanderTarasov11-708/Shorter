from django.test import TestCase

from ShorterProject import models


class LinkModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        link_db = models.Link()
        link_db.link = 'https://www.google.com/'
        link_db.hash = link_db.get_hash()
        link_db.save()

    def test_original_label(self):
        """ Testing the "original" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('link').verbose_name
        self.assertEquals(field_label, 'link')

    def test_hash_label(self):
        """ Testing the "hash" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('hash').verbose_name
        self.assertEquals(field_label, 'hash')

    def test_hits_label(self):
        """ Testing the "hits" field translation to human language"""
        link = models.Link.objects.get(id=1)
        field_label = link._meta.get_field('hits').verbose_name
        self.assertEquals(field_label, 'hits')

    def test_hash_max_length(self):
        """ Testing the max length of the 'hash' field"""
        link = models.Link.objects.get(id=1)
        max_length = link._meta.get_field('hash').max_length
        self.assertEquals(max_length, 6)

    def test_hits_default_value(self):
        """ Testing the default value of the 'hits' field"""
        link = models.Link.objects.get(id=1)
        self.assertEquals(link.hits, 0)
