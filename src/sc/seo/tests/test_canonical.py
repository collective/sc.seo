# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from sc.seo.behaviors.canonical import ICanonicalURL
from sc.seo.testing import SC_SEO_INTEGRATION_TESTING  # noqa
from zope.component import queryUtility

import unittest2 as unittest


class ICanonicalURLTest(unittest.TestCase):

    layer = SC_SEO_INTEGRATION_TESTING
    behavior_name = 'sc.seo.behaviors.canonical.ICanonicalURL'

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        fti = queryUtility(IDexterityFTI, name='Document')
        behaviors = list(fti.behaviors)
        behaviors.append(self.behavior_name)
        fti.behaviors = tuple(behaviors)

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.behavior_name)
        self.assertIsNotNone(registration)

    def test_adapt_content(self):
        self.portal.invokeFactory('Document', 'doc-1')
        doc = self.portal['doc-1']
        behavior = ICanonicalURL(doc)
        self.assertIsNotNone(behavior)

    def test_canonical_url(self):
        self.portal.invokeFactory('Document', 'doc-1')
        doc = self.portal['doc-1']
        behavior = ICanonicalURL(doc)
        self.assertEqual(behavior.canonical_url, None)
        behavior.canonical_url = u'http://www.simplesconsultoria.com.br/'
        self.assertEqual(behavior.canonical_url, u'http://www.simplesconsultoria.com.br/')

    def test_viewlet(self):
        self.portal.invokeFactory('Document', 'doc-1')
        doc = self.portal['doc-1']
        view = api.content.get_view('view', doc, self.request)
        rendered = view()
        self.assertIn('rel="canonical" href="http://nohost', rendered)
        behavior = ICanonicalURL(doc)
        behavior.canonical_url = u'http://www.simplesconsultoria.com.br/'
        view = api.content.get_view('view', doc, self.request)
        rendered = view()
        self.assertIn('rel="canonical" href="http://www.simplesconsultoria', rendered)
