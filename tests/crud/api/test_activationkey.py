"""Unit tests for the ``activation_keys`` paths."""

from fauxfactory import gen_string
from nailgun import entities
from requests.exceptions import HTTPError
from robottelo.test import APITestCase


class ActivationKeys(APITestCase):
    """Tests for the ``activation_keys`` path."""

    @classmethod
    def setUpClass(cls):  # noqa
        """Set up a default organization for all tests."""
        super(ActivationKeys, cls).setUpClass()
        cls.org = entities.Organization().create()

    def test_positive_create(self):
        """@Test: Create an activation key providing the initial name.

        @Assert: Activation key is created and contains provided name.

        @Feature: ActivationKey

        """
        name = gen_string('utf8', 30)
        act_key = entities.ActivationKey(
            organization=self.org, name=name).create()
        self.assertEqual(name, act_key.name)

    def test_negative_create(self):
        """@Test: Create activation key providing an invalid initial name.
        set.

        @Assert: Activation key is not created

        @Feature: ActivationKey

        """
        name = gen_string('utf8', 300)
        with self.assertRaises(HTTPError):
            entities.ActivationKey(
                organization=self.org, name=name).create()

    def test_positive_update(self):
        """@Test: Create activation key providing the initial name, then update
        its name to another valid name.

        @Assert: Activation key is created, and its name can be updated.

        @Feature: ActivationKey

        """
        act_key = entities.ActivationKey(organization=self.org).create()

        new_name = gen_string('utf8', 30)
        updated = entities.ActivationKey(
            id=act_key.id, name=new_name).update(['name'])
        self.assertEqual(new_name, updated.name)
        self.assertNotEqual(act_key.name, updated.name)

    def test_negative_update(self):
        """@Test: Create activation key then update its name to an invalid name.

        @Assert: Activation key is created, and its name is not updated.

        @Feature: ActivationKey

        """
        act_key = entities.ActivationKey(organization=self.org).create()
        name = act_key.name
        new_name = gen_string('utf8', 300)
        with self.assertRaises(HTTPError):
            entities.ActivationKey(
                id=act_key.id, name=new_name).update(['name'])
        act_key = entities.ActivationKey(id=act_key.id).read()
        self.assertNotEqual(act_key.name, new_name)
        self.assertEqual(name, act_key.name)

    def test_positive_delete(self):
        """@Test: Create activation key and then delete it.

        @Assert: Activation key is successfully deleted.

        @Feature: ActivationKey

        """
        act_key = entities.ActivationKey(organization=self.org).create()
        act_key.delete()
        with self.assertRaises(HTTPError):
            entities.ActivationKey(id=act_key.id).read()
