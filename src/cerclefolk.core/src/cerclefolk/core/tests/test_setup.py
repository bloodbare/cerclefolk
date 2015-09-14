# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cerclefolk.core.testing import CERCLEFOLK_CORE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that cerclefolk.core is properly installed."""

    layer = CERCLEFOLK_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cerclefolk.core is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('cerclefolk.core'))

    def test_browserlayer(self):
        """Test that ICerclefolkCoreLayer is registered."""
        from cerclefolk.core.interfaces import ICerclefolkCoreLayer
        from plone.browserlayer import utils
        self.assertIn(ICerclefolkCoreLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CERCLEFOLK_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cerclefolk.core'])

    def test_product_uninstalled(self):
        """Test if cerclefolk.core is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('cerclefolk.core'))

    def test_browserlayer_removed(self):
        """Test that ICerclefolkCoreLayer is removed."""
        from cerclefolk.core.interfaces import ICerclefolkCoreLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICerclefolkCoreLayer, utils.registered_layers())
