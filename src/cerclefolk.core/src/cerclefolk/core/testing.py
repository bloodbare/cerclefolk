# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cerclefolk.core


class CerclefolkCoreLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=cerclefolk.core)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cerclefolk.core:default')


CERCLEFOLK_CORE_FIXTURE = CerclefolkCoreLayer()


CERCLEFOLK_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CERCLEFOLK_CORE_FIXTURE,),
    name='CerclefolkCoreLayer:IntegrationTesting'
)


CERCLEFOLK_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CERCLEFOLK_CORE_FIXTURE,),
    name='CerclefolkCoreLayer:FunctionalTesting'
)


CERCLEFOLK_CORE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CERCLEFOLK_CORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CerclefolkCoreLayer:AcceptanceTesting'
)
