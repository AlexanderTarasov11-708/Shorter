from django.test import TestCase, Client
from django.urls import reverse

from ShorterProject import models
from ShorterProject.models import Link


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        link_db = models.Link()
        link_db.original = 'https://www.google.com/'
        link_db.hash = link_db.get_hash()
        link_db.save()
        link_db = models.Link()
        link_db.original = 'https://www.google.com/'
        link_db.hash = link_db.get_hash()
        link_db.save()

    def test_call_view_index_get(self):
        """ Testing the "index" view with GET method"""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertNotContains(response, 'Сокращенная ссылка:')

    def test_call_view_index_post_empty_link(self):
        """ Testing the "index" view with POST method with empty link"""
        url = reverse('home')
        response = self.client.post(url, {'url': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Введите валидный Url')

    def test_call_view_index_post_wrong_link(self):
        """ Testing the "index" view with POST method with invalid link"""
        url = reverse('home')
        response = self.client.post(url, {'url': 'https://sdfsdfsdf   www.google.com/'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Введите валидный Url')

    def test_call_view_index_post_normal_link(self):
        """ Testing the "index" view with POST method with valid link"""
        url = reverse('home')
        response = self.client.post(url, {'url': 'https://www.google.com/'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Сокращённый URL: ')

    def test_call_view_all_get(self):
        """ Testing the "all" view with GET method"""
        url = reverse('all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'links.html')
        all_links = response.context['all_results']
        self.assertCountEqual(all_links, Link.objects.all())
