from django.test import TestCase

# Create your tests here.
from rango.models import Category

from django.core.urlresolvers import reverse

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """ test_ensure_views_are_positive должна возвращать True """
        cat=Category(name="test", views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views>=0), True)
    def test_slug_line_creation(self):
        """ проверяет верность/правильность slug """
        cat=Category(name="Random Category String")
        cat.save()
        self.assertEqual(cat.slug, "random-category-string")

class IndexViewTests(TestCase):
    """ тест представлений """
    def test_index_view_with_no_categories(self):
        response=self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], [])
