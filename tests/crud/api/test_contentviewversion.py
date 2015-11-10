"""Unit tests for the ``content view versions`` paths."""

from fauxfactory import gen_string
from nailgun import entities
from requests.exceptions import HTTPError
from robottelo.test import APITestCase


class ContentViewFilters(APITestCase):
    """Tests for the ``content view versions`` path."""

    @classmethod
    def setUpClass(cls):
        """Init single organization, product and repository for all tests"""
        super(ContentViewFilters, cls).setUpClass()
        cls.org = entities.Organization().create()

    def setUp(self):
        """Init content view with repo per each test"""
        super(ContentViewFilters, self).setUp()
        self.content_view = entities.ContentView(
            organization=self.org,
        ).create()

    def test_positive_create(self):
        """@Test: Create a content view version.

        @Assert: Content View Version is created.

        @Feature: Content View Version

        """
        # Fetch content view for latest information
        cv = self.content_view.read()
        # No versions should be available yet
        self.assertEqual(len(cv.version), 0)

        # Publish existing content view
        cv.publish()
        # Fetch it again
        cv = cv.read()
        self.assertGreater(len(cv.version), 0)

    def test_negative_create(self):
        """@Test: Create content view version using the 'Default Content View'.
        set.

        @Assert: Content View Version is not created

        @Feature: Content View Version

        """
        # The default content view cannot be published
        # TODO: Use the organization's 'Default Content View'.
        cv = entities.ContentView(id=1).read()
        with self.assertRaises(HTTPError):
            cv.publish()

    def test_positive_delete(self):
        """@Test: Create content view version and then delete it.

        @Assert: Content View Version is successfully deleted.

        @Feature: Content View Version

        """
        # Fetch content view for latest information
        cv = self.content_view.read()
        # No versions should be available yet
        self.assertEqual(len(cv.version), 0)

        # Publish existing content view
        cv.publish()
        # Fetch it again
        cv = cv.read()
        self.assertGreater(len(cv.version), 0)

        # Delete it
        cvv = cv.version[0].read()
        # Delete the content-view version from selected env
        cv.delete_from_environment(cvv.environment[0].id)
        # Delete the version
        cv.version[0].delete()
        # Make sure that content view version is really removed
        self.assertEqual(len(cv.read().version), 0)
