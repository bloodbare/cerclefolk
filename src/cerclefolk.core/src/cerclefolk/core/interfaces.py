# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from cerclefolk.core import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.directives import form


class ICerclefolkCoreLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IEsdeveniment(Interface):

    inscriptions_available = schema.Bool(title=_(u"Hi ha inscripcions?"),
                                         description=_(u""),
                                         required=False)

    start_inscription = schema.Datetime(title=_(u"Inici inscripció"),
                                        description=_(u""),
                                        required=False)

    end_inscription = schema.Datetime(title=_(u"Fi inscripció"),
                                      description=_(u""),
                                      required=False)

@form.default_value(field=IEsdeveniment['start_inscription'])
def start_inscriptionDefaultValue(data):
    return datetime.datetime.today()


@form.default_value(field=IEsdeveniment['end_inscription'])
def end_inscriptionDefaultValue(data):
    return datetime.datetime.today()