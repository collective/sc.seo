# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import sc.seo


class ScSeoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=sc.seo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'sc.seo:default')


SC_SEO_FIXTURE = ScSeoLayer()


SC_SEO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SC_SEO_FIXTURE,),
    name='ScSeoLayer:IntegrationTesting'
)


SC_SEO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SC_SEO_FIXTURE,),
    name='ScSeoLayer:FunctionalTesting'
)


SC_SEO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SC_SEO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='ScSeoLayer:AcceptanceTesting'
)
