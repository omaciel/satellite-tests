"""Unit tests for the ``architectures`` paths."""

from fauxfactory import gen_string
from nailgun import entities
from requests.exceptions import HTTPError
from robottelo.test import APITestCase


class Architectures(APITestCase):
    """Tests for the ``architectures`` path."""

    def test_positive_create(self):
        """@Test: Create an architecture providing the initial name.

        @Assert: Architecture is created and contains provided name.

        @Feature: Architecture

        """
        name = gen_string('utf8', 30)
        arch = entities.Architecture(name=name).create()
        self.assertEqual(name, arch.name)

    def test_negative_create(self):
        """@Test: Create architecture providing an invalid initial name.
        set.

        @Assert: Architecture is not created

        @Feature: Architecture

        """
        with self.assertRaises(HTTPError):
            entities.Architecture(name=gen_string('utf8', 300)).create()

    def test_positive_update(self):
        """@Test: Create architecture then update its name to another
        valid name.

        @Assert: Architecture is created, and its name can be updated.

        @Feature: Architecture

        """
        arch = entities.Architecture().create()

        new_name = gen_string('utf8', 30)
        updated = entities.Architecture(
            id=arch.id, name=new_name).update(['name'])
        self.assertEqual(new_name, updated.name)
        self.assertNotEqual(arch.name, updated.name)

    def test_negative_update(self):
        """@Test: Create architecture then update its name to an invalid name.

        @Assert: architecture is created, and its name is not updated.

        @Feature: Architecture

        """
        arch = entities.Architecture().create()
        name = arch.name
        new_name = gen_string('utf8', 300)
        with self.assertRaises(HTTPError):
            entities.Architecture(
                id=arch.id, name=new_name).update(['name'])
        arch = entities.Architecture(id=arch.id).read()
        self.assertNotEqual(arch.name, new_name)
        self.assertEqual(name, arch.name)

    def test_positive_delete(self):
        """@Test: Create architecture and then delete it.

        @Assert: architecture is successfully deleted.

        @Feature: Architecture

        """
        arch = entities.Architecture().create()
        arch.delete()
        with self.assertRaises(HTTPError):
            entities.Architecture(id=arch.id).read()
