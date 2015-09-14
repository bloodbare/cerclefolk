# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from cerclefolk.core.testing import CERCLEFOLK_CORE_INTEGRATION_TESTING  # noqa
from cerclefolk.core.interfaces import IEsdeveniment

import unittest2 as unittest


class EsdevenimentIntegrationTest(unittest.TestCase):

    layer = CERCLEFOLK_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Esdeveniment')
        schema = fti.lookupSchema()
        self.assertEqual(IEsdeveniment, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Esdeveniment')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Esdeveniment')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IEsdeveniment.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('Esdeveniment', 'Esdeveniment')
        self.assertTrue(
            IEsdeveniment.providedBy(self.portal['Esdeveniment'])
        )
