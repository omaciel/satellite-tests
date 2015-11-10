"""Unit tests for the ``content view filters`` paths."""

from fauxfactory import gen_string
from nailgun import entities
from requests.exceptions import HTTPError
from robottelo.test import APITestCase


class ContentViewFilters(APITestCase):
    """Tests for the ``content view filters`` path."""

    @classmethod
    def setUpClass(cls):
        """Init single organization, product and repository for all tests"""
        super(ContentViewFilters, cls).setUpClass()
        cls.org = entities.Organization().create()
        cls.product = entities.Product(organization=cls.org).create()
        cls.repo = entities.Repository(product=cls.product).create()
        cls.repo.sync()

    def setUp(self):
        """Init content view with repo per each test"""
        super(ContentViewFilters, self).setUp()
        self.content_view = entities.ContentView(
            organization=self.org,
        ).create()
        self.content_view.repository = [self.repo]
        self.content_view.update(['repository'])

    def test_positive_create(self):
        """@Test: Create a content view filter providing the initial name.

        @Assert: Content View Filter is created and contains provided name.

        @Feature: Content View Filter

        """
        name = gen_string('utf8', 30)
        cvf = entities.RPMContentViewFilter(
            content_view=self.content_view,
            name=name,
        ).create()
        self.assertEqual(name, cvf.name)

    def test_negative_create(self):
        """@Test: Create content view filter providing an invalid initial name.
        set.

        @Assert: Content View Filter is not created

        @Feature: Content View Filter

        """
        with self.assertRaises(HTTPError):
            entities.RPMContentViewFilter(
                content_view=self.content_view,
                name=gen_string('utf8', 300),
            ).create()

    def test_positive_update(self):
        """@Test: Create content view filter then update its name to another
        valid name.

        @Assert: Content View Filter is created, and its name can be
        updated.

        @Feature: Content View Filter

        """
        cvf = entities.RPMContentViewFilter(
            content_view=self.content_view).create()

        new_name = gen_string('utf8', 30)
        updated = entities.RPMContentViewFilter(
            id=cvf.id, name=new_name).update(['name'])
        self.assertEqual(new_name, updated.name)
        self.assertNotEqual(cvf.name, updated.name)

    def test_negative_update(self):
        """@Test: Create content view filter then update its name to an
        invalid name.

        @Assert: Content View Filter is created, and its name is not
        updated.

        @Feature: Content View Filter

        """
        cvf = entities.RPMContentViewFilter(
            content_view=self.content_view).create()

        name = cvf.name
        new_name = gen_string('utf8', 300)
        with self.assertRaises(HTTPError):
            entities.RPMContentViewFilter(
                id=cvf.id, name=new_name).update(['name'])
        cvf = entities.RPMContentViewFilter(id=cvf.id).read()
        self.assertNotEqual(cvf.name, new_name)
        self.assertEqual(name, cvf.name)

    def test_positive_delete(self):
        """@Test: Create content view filter and then delete it.

        @Assert: Content View Filter is successfully deleted.

        @Feature: Content View Filter

        """
        cvf = entities.RPMContentViewFilter(
            content_view=self.content_view).create()
        cvf.delete()
        with self.assertRaises(HTTPError):
            entities.RPMContentViewFilter(id=cvf.id).read()
