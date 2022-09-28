from django.test import TestCase
from django.urls import reverse, resolve



class TestUrls(TestCase):
  def test_post_index_url(self):
    view = resolve('/twitteranalytics/')
