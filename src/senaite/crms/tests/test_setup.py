# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from senaite.crms.testing import SENAITE_CRMS_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that senaite.crms is properly installed."""

    layer = SENAITE_CRMS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if senaite.crms is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'senaite.crms'))

    def test_browserlayer(self):
        """Test that ISenaiteCrmsLayer is registered."""
        from senaite.crms.interfaces import (
            ISenaiteCrmsLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ISenaiteCrmsLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = SENAITE_CRMS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['senaite.crms'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if senaite.crms is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'senaite.crms'))

    def test_browserlayer_removed(self):
        """Test that ISenaiteCrmsLayer is removed."""
        from senaite.crms.interfaces import \
            ISenaiteCrmsLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ISenaiteCrmsLayer,
            utils.registered_layers())
