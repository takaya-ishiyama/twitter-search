from twitteranalytics.views import *
from django.views import generic
from django.test import TestCase
from django.urls import reverse


class IndexTests(TestCase):
  """IndexViewのテストクラス"""

  def test_get(self):
    """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
    response = self.client.get(reverse('twitteranalytics:index'))
    self.assertEqual(response.status_code, 200)