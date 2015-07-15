# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from plone.dexterity.interfaces import IDexterityFTI
from sc.seo.behaviors.metarobots import IMetaRobots
from sc.seo.testing import SC_SEO_INTEGRATION_TESTING  # noqa
from zope.component import queryUtility

import unittest2 as unittest


class IMetaRobotsTest(unittest.TestCase):

    layer = SC_SEO_INTEGRATION_TESTING
    behavior_name = 'sc.seo.behaviors.metarobots.IMetaRobots'

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
        behavior = IMetaRobots(doc)
        self.assertIsNotNone(behavior)

    def test_meta_robots(self):
        self.portal.invokeFactory('Document', 'doc-1')
        doc = self.portal['doc-1']
        behavior = IMetaRobots(doc)
        self.assertEqual(behavior.robots, None)
        behavior.robots = [u'nofollow', ]
        self.assertEqual(behavior.robots, [u'nofollow', ])

    def test_viewlet(self):
        self.portal.invokeFactory('Document', 'doc-1')
        doc = self.portal['doc-1']
        view = api.content.get_view('view', doc, self.request)
        rendered = view()
        self.assertIn('<meta name="robots" content="all', rendered)
        behavior = IMetaRobots(doc)
        behavior.robots = [u'nofollow', ]
        view = api.content.get_view('view', doc, self.request)
        rendered = view()
        self.assertIn('<meta name="robots" content="nofollow', rendered)
