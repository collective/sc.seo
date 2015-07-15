# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from sc.seo.testing import SC_SEO_INTEGRATION_TESTING  # noqa

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that sc.seo is properly installed."""

    layer = SC_SEO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if sc.seo is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('sc.seo'))

    def test_browserlayer(self):
        """Test that ISCSEOLayer is registered."""
        from sc.seo.interfaces import ISCSEOLayer
        from plone.browserlayer import utils
        self.assertIn(ISCSEOLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = SC_SEO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['sc.seo'])

    def test_product_uninstalled(self):
        """Test if sc.seo is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('sc.seo'))

    def test_browserlayer_removed(self):
        """Test that ISCSEOLayer is removed."""
        from sc.seo.interfaces import ISCSEOLayer
        from plone.browserlayer import utils
        self.assertNotIn(ISCSEOLayer, utils.registered_layers())
