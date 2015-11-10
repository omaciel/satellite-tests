"""Unit tests for the ``content views`` paths."""

from fauxfactory import gen_string
from nailgun import entities
from requests.exceptions import HTTPError
from robottelo.test import APITestCase


class ContentView(APITestCase):
    """Tests for the ``content views`` path."""

    def test_positive_create(self):
        """@Test: Create a content view providing the initial name.

        @Assert: Content View is created and contains provided name.

        @Feature: Content View

        """
        name = gen_string('utf8', 30)
        cv = entities.ContentView(name=name).create()
        self.assertEqual(name, cv.name)

    def test_negative_create(self):
        """@Test: Create content view providing an invalid initial name.
        set.

        @Assert: Content View is not created

        @Feature: Content View

        """
        with self.assertRaises(HTTPError):
            entities.ContentView(name=gen_string('utf8', 300)).create()

    def test_positive_update(self):
        """@Test: Create content view providing the initial name, then update
        its name to another valid name.

        @Assert: Content View is created, and its name can be
        updated.

        @Feature: Content View

        """
        cv = entities.ContentView().create()

        new_name = gen_string('utf8', 30)
        updated = entities.ContentView(
            id=cv.id, name=new_name).update(['name'])
        self.assertEqual(new_name, updated.name)
        self.assertNotEqual(cv.name, updated.name)

    def test_negative_update(self):
        """@Test: Create content view then update its name to an
        invalid name.

        @Assert: Content View is created, and its name is not
        updated.

        @Feature: Content View

        """
        cv = entities.ContentView().create()
        name = cv.name
        new_name = gen_string('utf8', 300)
        with self.assertRaises(HTTPError):
            entities.ContentView(
                id=cv.id, name=new_name).update(['name'])
        cv = entities.ContentView(id=cv.id).read()
        self.assertNotEqual(cv.name, new_name)
        self.assertEqual(name, cv.name)

    def test_positive_delete(self):
        """@Test: Create content view and then delete it.

        @Assert: Content View is successfully deleted.

        @Feature: Content View

        """
        cv = entities.ContentView().create()
        cv.delete()
        with self.assertRaises(HTTPError):
            entities.ContentView(id=cv.id).read()
