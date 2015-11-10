"""Unit tests for the ``configuration templates`` paths."""

from fauxfactory import gen_string
from nailgun import entities
from requests.exceptions import HTTPError
from robottelo.test import APITestCase


class ConfigurationTemplates(APITestCase):
    """Tests for the ``configuration templates`` path."""

    def test_positive_create(self):
        """@Test: Create a configuration template providing the initial name.

        @Assert: Configuration Template is created and contains provided name.

        @Feature: Configuration Template

        """
        name = gen_string('utf8', 30)
        c_temp = entities.ConfigTemplate(name=name).create()
        self.assertEqual(name, c_temp.name)

    def test_negative_create(self):
        """@Test: Create configuration template providing an invalid initial name.
        set.

        @Assert: Configuration Template is not created

        @Feature: Configuration Template

        """
        with self.assertRaises(HTTPError):
            entities.ConfigTemplate(name=gen_string('utf8', 300)).create()

    def test_positive_update(self):
        """@Test: Create configuration template providing the initial name, then update
        its name to another valid name.

        @Assert: Configuration Template is created, and its name can be
        updated.

        @Feature: Configuration Template

        """
        c_temp = entities.ConfigTemplate().create()

        new_name = gen_string('utf8', 30)
        updated = entities.ConfigTemplate(
            id=c_temp.id, name=new_name).update(['name'])
        self.assertEqual(new_name, updated.name)
        self.assertNotEqual(c_temp.name, updated.name)

    def test_negative_update(self):
        """@Test: Create configuration template then update its name to an
        invalid name.

        @Assert: Configuration Template is created, and its name is not
        updated.

        @Feature: Configuration Template

        """
        c_temp = entities.ConfigTemplate().create()
        name = c_temp.name
        new_name = gen_string('utf8', 300)
        with self.assertRaises(HTTPError):
            entities.ConfigTemplate(
                id=c_temp.id, name=new_name).update(['name'])
        c_temp = entities.ConfigTemplate(id=c_temp.id).read()
        self.assertNotEqual(c_temp.name, new_name)
        self.assertEqual(name, c_temp.name)

    def test_positive_delete(self):
        """@Test: Create configuration template and then delete it.

        @Assert: Configuration Template is successfully deleted.

        @Feature: Configuration Template

        """
        c_temp = entities.ConfigTemplate().create()
        c_temp.delete()
        with self.assertRaises(HTTPError):
            entities.ConfigTemplate(id=c_temp.id).read()
