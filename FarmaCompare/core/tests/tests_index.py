from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url as r

class IndexTestCase(TestCase):
    
    def setUp(self):
        self.resp = self.client.get(r('core:index'), follow=True)
    
    def test_index_vies_seccess(self):
        self.assertEqual(self.resp.status_code, 200)
    
    def test_template_used(self):
        self.assertTemplateUsed(self.resp, 'index.html')